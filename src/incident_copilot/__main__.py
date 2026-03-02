"""Package entry point — delegates to the CLI main()."""

from incident_copilot.main import main
import sys

if __name__ == "__main__":
    sys.exit(main())
