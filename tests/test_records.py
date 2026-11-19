"""`just new-record`: a minted id by default, never an id already in use, and a valid record."""

import re

import pytest
import yaml

from dentamech import records
from dentamech.paths import SLUG


@pytest.fixture
def records_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(records, "RECORDS_DIR", tmp_path)
    return tmp_path


UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def test_mint_id_is_unique_and_in_the_mechs_namespace():
    a, b = records.mint_id(), records.mint_id()
    assert a != b
    assert re.fullmatch(re.escape(SLUG) + ":" + UUID, a)


def test_an_id_in_use_is_refused(records_dir, capsys):
    (records_dir / "alpha.yaml").write_text(yaml.safe_dump({"id": "X:1", "name": "Alpha"}))
    assert records.main(["new", "--id", "X:1", "--name", "Beta", "--term-label", "beta",
                         "--category", "OTHER"]) == 1
    assert "id X:1 is already used by" in capsys.readouterr().out
    assert sorted(p.name for p in records_dir.iterdir()) == ["alpha.yaml"]


def test_without_an_id_one_is_minted(records_dir, monkeypatch):
    # Capture what would be validated and written: a designed schema may need
    # more than a name, which is not what this test is about.
    written = []
    monkeypatch.setattr(records, "write_validated_record", lambda data, path, **_: written.append(data))
    assert records.main(["new", "--name", "Alpha", "--category", "OTHER"]) == 0
    assert records.main(["new", "--name", "Beta", "--category", "OTHER"]) == 0
    a, b = (d["id"] for d in written)
    assert a != b and re.fullmatch(re.escape(SLUG) + ":" + UUID, a)
    assert "record_term" not in written[0]


def _new(*args) -> list[str]:
    return ["new", *args, "--apply"]


def test_category_is_required(records_dir):
    with pytest.raises(SystemExit):
        records.main(["new", "--name", "Alpha"])


def test_choices_come_from_the_schema():
    assert "POLYMER" in records.enum_values("MaterialCategoryEnum")
    assert records.enum_values("MaterialPurposeEnum") == ["PREVENTIVE", "AUXILIARY", "RESTORATIVE"]


def test_a_minted_id_scaffolds_a_valid_record(records_dir):
    # Through the real write_validated_record: the scaffold must pass validation.
    assert records.main(_new("--name", "Denture base polymer", "--category", "POLYMER")) == 0
    data = yaml.safe_load((records_dir / "denture_base_polymer.yaml").read_text())
    assert data["category"] == "POLYMER" and data["status"] == "DRAFT"
    assert "purpose" not in data and "experimental" not in data


def test_an_ontology_id_scaffolds_a_valid_record(records_dir):
    assert records.main(_new("--id", "OHD:0001006", "--name", "Glass ionomer cement",
                             "--term-label", "glass ionomer cement dental restoration material",
                             "--category", "CEMENT")) == 0
    data = yaml.safe_load((records_dir / "glass_ionomer_cement.yaml").read_text())
    assert data["record_term"] == {"id": "OHD:0001006",
                                   "label": "glass ionomer cement dental restoration material"}
    keys = list(data)
    assert keys.index("record_term") < keys.index("status") < keys.index("category")


def test_an_experimental_record_needs_its_classification(records_dir, capsys):
    base = ("--name", "Experimental composite", "--category", "RESIN_COMPOSITE", "--experimental")
    assert records.main(_new(*base)) == 1
    assert "an experimental record must give purpose" in capsys.readouterr().out
    assert records.main(_new(*base, "--purpose", "RESTORATIVE")) == 1
    assert "must give restorative_class" in capsys.readouterr().out
    assert not list(records_dir.iterdir())
    assert records.main(_new(*base, "--purpose", "RESTORATIVE", "--restorative-class", "COMPOSITE")) == 0
    data = yaml.safe_load((records_dir / "experimental_composite.yaml").read_text())
    assert (data["experimental"], data["purpose"], data["restorative_class"]) == \
        (True, "RESTORATIVE", "COMPOSITE")


def test_a_contradictory_class_is_refused(records_dir, capsys):
    assert records.main(_new("--name", "Odd", "--category", "METAL", "--purpose", "RESTORATIVE",
                             "--restorative-class", "CERAMIC")) == 1
    assert "contradicts category METAL" in capsys.readouterr().out
