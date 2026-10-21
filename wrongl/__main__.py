"""Allow `python -m wrongl`."""
from wrongl.app import main

if __name__ == "__main__":
    raise SystemExit(main())