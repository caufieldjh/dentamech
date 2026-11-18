"""linkml-reference-validator's command line, with this Mech's sources registered.

``python -m dentamech.lrv validate data ...`` takes the same arguments as
``linkml-reference-validator``. The justfile calls the validator through this,
so ``CFR:`` references are fetched and checked (see ``refsources``).
"""

from dentamech.refsources import register


def main() -> None:
    register()
    from linkml_reference_validator.cli import main as validator_main

    validator_main()


if __name__ == "__main__":
    main()
