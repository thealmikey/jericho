"""Simple verifier script to exercise the Pd Orchestra via OSC.

Usage (PowerShell):
  python src/verify.py           # use detected `pd` if available
  python src/verify.py --no-pd   # skip starting Pd, still send OSC messages
  python src/verify.py --pd C:\\Program Files\\Pd\\pd.exe   # use specific pd executable

The script will:
- optionally start Pd (if found or provided)
- send a /start, a few /progress updates (0,20,50,80,100)
- send a sample play and a /finish (success)

This is intended as a friendly smoke-test that plays gentle test notes when Pd is available.
"""
import argparse
import time
import logging
from pd_orchestra import PdOrchestra

logging.basicConfig(level=logging.INFO)


def run_verifier(pd_path: str | None, no_pd: bool) -> None:
    pd_exec = None
    if no_pd:
        pd_exec = None
    elif pd_path:
        pd_exec = pd_path

    print("Starting verifier. Pd executable:", pd_exec or "(auto-detect or skipped)")
    orchestra = PdOrchestra(pd_executable=pd_exec)

    try:
        print("-> starting session (test)")
        orchestra.start_session("verify")

        steps = [0, 20, 50, 80, 100]
        for pct in steps:
            print(f"-> sending /progress {pct}")
            orchestra.update_progress(pct, message=f"verify {pct}")
            time.sleep(0.8)

        # try one-shot sample (if available)
        print("-> sending one-shot 'ding' and 'tada' cues")
        orchestra.play_one_shot("ding")
        time.sleep(0.3)
        orchestra.play_one_shot("tada")
        time.sleep(0.6)

        print("-> finishing session (success=true)")
        orchestra.finish_session(True)

        print("Verifier complete — listen for gentle test notes in Pd (if running).")
    except Exception as ex:
        print("Verifier encountered an error:", ex)


def main():
    parser = argparse.ArgumentParser(description="Verify Pd Orchestra and OSC path")
    parser.add_argument("--pd", help="Path to pd executable (overrides auto-detect)")
    parser.add_argument("--no-pd", help="Do not attempt to start Pd (send OSC only)", action="store_true")
    args = parser.parse_args()

    run_verifier(args.pd, args.no_pd)


if __name__ == "__main__":
    main()
