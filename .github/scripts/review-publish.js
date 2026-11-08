// Post the review the review agent returned. No model runs here, and no code
// from the PR: this checks the review against the PR as it is now and posts
// it, so the agent's output reaches nothing it was not meant to.

const MARKER = 'mech-review:v1';
const SEVERITIES = ['error', 'warning', 'note'];
const CHECKLIST = [
  ['qc', '`just qc` would pass'],
  ['quotes', 'every quote supports its claim'],
  ['terms', 'terms are correct and specific'],
  ['scope', 'records are in scope and not duplicates'],
  ['history', 'history records are present and filled in'],
];

function clean(text, max = 6000) {
  // One agent's words must not summon people or other agents.
  return String(text ?? '').replace(/@/g, '@​').trim().slice(0, max);
}

function shape(review) {
  if (!review || typeof review !== 'object') return null;
  const findings = (Array.isArray(review.findings) ? review.findings : [])
    .filter(f => f && SEVERITIES.includes(f.severity) && String(f.body ?? '').trim())
    .slice(0, 50);
  return {
    verdict: review.verdict === 'approve' ? 'approve' : 'request_changes',
    checklist: review.checklist && typeof review.checklist === 'object' ? review.checklist : {},
    summary: clean(review.summary) || '(no summary)',
    findings,
  };
}

function listed(f) {
  const where = f.path ? ` \`${clean(f.path, 300)}${Number.isSafeInteger(f.line) ? `:${f.line}` : ''}\`` : '';
  return `- **${f.severity}**${where}: ${clean(f.body, 3000)}`;
}

function body(r, inlineFindings, note) {
  const lines = CHECKLIST.map(([key, text]) => `- [${r.checklist[key] === true ? 'x' : ' '}] ${text}`);
  lines.push('', r.summary);
  const rest = r.findings.filter(f => !inlineFindings.includes(f));
  if (rest.length) lines.push('', '**Findings**', '', ...rest.map(listed));
  if (note) lines.push('', `_${note}_`);
  lines.push('', `<!-- ${MARKER} -->`);
  return lines.join('\n');
}

// An approving verdict clears this reviewer's own earlier blocks. GitHub
// keeps a reviewer's last CHANGES_REQUESTED in force until that reviewer
// approves, and a COMMENT review never lifts it. So when an approval is
// refused (Actions may not approve here, and no reviewer App is set), the
// PR would stay blocked by a review whose findings are fixed. Dismissing the
// reviewer's own blocking reviews is what lets it say "no more changes
// needed" either way. Other reviewers' reviews, people's above all, are never
// touched.
async function clearOwnBlocks(github, repo, pr, posted, { log = console.log, warn = console.warn } = {}) {
  const login = posted?.user?.login;
  if (!login) { warn('Could not tell who posted the review; earlier blocking reviews left as they are.'); return 0; }
  const reviews = await github.paginate(github.rest.pulls.listReviews, { ...repo, pull_number: pr, per_page: 100 });
  let cleared = 0;
  for (const old of reviews) {
    if (old.id === posted.id || old.user?.login !== login || old.state !== 'CHANGES_REQUESTED') continue;
    try {
      await github.rest.pulls.dismissReview({
        ...repo, pull_number: pr, review_id: old.id,
        message: `Superseded by review ${posted.id}, which found nothing blocking.`,
      });
      cleared += 1;
    } catch (err) {
      warn(`Could not dismiss earlier review ${old.id}: ${err.message}`);
    }
  }
  if (cleared) log(`Dismissed ${cleared} earlier blocking review(s) by ${login} on PR #${pr}.`);
  return cleared;
}

async function publish(github, repo, review, { pr, sha, log = console.log, warn = console.warn } = {}) {
  const r = shape(review);
  if (!r) { warn('No review to post: the agent returned nothing usable.'); return { posted: null }; }
  if (!Number.isSafeInteger(pr) || !/^[0-9a-f]{40}$/.test(String(sha))) {
    warn('No review posted: the PR number or the reviewed commit is missing.'); return { posted: null };
  }
  const { data: pull } = await github.rest.pulls.get({ ...repo, pull_number: pr });
  if (pull.state !== 'open') { warn(`PR #${pr} is ${pull.state}; no review posted.`); return { posted: null }; }
  if (pull.head.repo?.full_name !== `${repo.owner}/${repo.repo}`) {
    warn(`PR #${pr} comes from a fork; no review posted.`); return { posted: null };
  }
  if (pull.head.sha !== sha) {
    warn(`PR #${pr} moved on to ${pull.head.sha.slice(0, 7)} after the review of ${sha.slice(0, 7)}; ` +
         'no review posted. Comment /review to review the new commit.');
    return { posted: null };
  }

  // Blocking findings decide the event, whatever the verdict says; the
  // verdict can only make a review stricter.
  const blocking = r.findings.some(f => f.severity !== 'note');
  const event = blocking || r.verdict === 'request_changes' ? 'REQUEST_CHANGES' : 'APPROVE';

  const files = new Set((await github.paginate(github.rest.pulls.listFiles, {
    ...repo, pull_number: pr, per_page: 100,
  })).map(f => f.filename));
  const inline = r.findings.filter(f => files.has(f.path) && Number.isSafeInteger(f.line) && f.line > 0);
  const comments = inline.map(f => ({
    path: f.path, line: f.line, side: 'RIGHT', body: `**${f.severity}**: ${clean(f.body, 3000)}`,
  }));

  const attempts = [
    { event, comments, inlineFindings: inline, note: '' },
    { event, comments: [], inlineFindings: [], note: '' },
  ];
  let lastError = null;
  for (const a of comments.length ? attempts : attempts.slice(1)) {
    try {
      const { data: posted } = await github.rest.pulls.createReview({
        ...repo, pull_number: pr, commit_id: sha, event: a.event,
        body: body(r, a.inlineFindings, a.note), comments: a.comments,
      });
      log(`Posted ${a.event} on PR #${pr} with ${a.comments.length} inline comment(s).`);
      const cleared = a.event === 'APPROVE' ? await clearOwnBlocks(github, repo, pr, posted, { log, warn }) : 0;
      return { posted: a.event, inline: a.comments.length, cleared };
    } catch (err) {
      lastError = err;
      warn(`${a.event} with ${a.comments.length} inline comment(s) failed: ${err.message}`);
    }
  }
  // GitHub refused the event itself, e.g. Actions may not approve here. Post
  // the same review as a comment, so the work is not lost, and say why.
  const note = `Posted as a comment: GitHub refused ${event} (${clean(lastError?.message, 300)}).`;
  const { data: posted } = await github.rest.pulls.createReview({
    ...repo, pull_number: pr, commit_id: sha, event: 'COMMENT', body: body(r, [], note), comments: [],
  });
  warn(note);
  // The verdict was an approval that GitHub would not take: still lift the
  // reviewer's own earlier blocks, so the PR is not left waiting on them.
  const cleared = event === 'APPROVE' ? await clearOwnBlocks(github, repo, pr, posted, { log, warn }) : 0;
  return { posted: 'COMMENT', inline: 0, cleared };
}

module.exports = { publish, shape, clearOwnBlocks, MARKER };
