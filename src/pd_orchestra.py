# src/pd_orchestra.py
import subprocess
import time
import os
import shutil
import logging
from pythonosc import udp_client
from pathlib import Path

log = logging.getLogger(__name__)


class PdOrchestra:
    def __init__(self, pd_executable: str | None = None):
        self.pd_process = None
        self.osc = udp_client.SimpleUDPClient("127.0.0.1", 4559)  # Pd receives on 4559
        self.patch_path = Path(__file__).parent.parent / "pd" / "orchestra.pd"
        self.samples_path = Path(__file__).parent.parent / "samples"
        # allow overriding executable (tests can pass None/"/dev/null")
        self.pd_executable = pd_executable or shutil.which("pd")
        if not self.pd_executable:
            log.warning("pd executable not found on PATH; running in headless/mock mode")
        else:
            try:
                self.start_pd()
            except FileNotFoundError:
                log.warning("Failed to start pd. Proceeding without Pd (FileNotFoundError)")
            except Exception:
                log.exception("Unexpected error while starting Pd subprocess")

    def start_pd(self):
        if not self.patch_path.exists():
            self.generate_patch()
        if not self.pd_executable:
            log.info("Skipping Pd start because executable is not configured")
            return
        cmd = [self.pd_executable, "-nogui", "-audiodev", "1,2", "-open", str(self.patch_path)]
        try:
            self.pd_process = subprocess.Popen(cmd)
            time.sleep(1.5)  # give Pd time to boot
        except FileNotFoundError:
            self.pd_process = None
            raise

    def generate_patch(self):
        # Write a basic Pure Data patch if none exists. Keep content minimal but functional.
        pd_content = """
#N canvas 10 10 900 700 10;
#X obj 10 10 declare -lib mrpeach;
#X obj 10 110 udpreceive 4559;
#X obj 10 140 oscparse;
#X obj 10 170 route /progress /finish /play_sample /ding /tada;
#X obj 10 200 s progress_val;
#X obj 10 260 loadbang;
#X obj 10 300 print pd_orchestra_loaded;
"""
        self.patch_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.patch_path, "w", encoding="utf8") as f:
                f.write(pd_content)
            log.info("Wrote generated Pure Data patch to %s", self.patch_path)
        except Exception:
            log.exception("Failed to write generated Pd patch")

    def start_session(self, task_name: str):
        self.osc.send_message("/start", 1.0)

    def update_progress(self, percent: float, message: str | None):
        self.osc.send_message("/progress", percent)
        # auto voice cues
        if int(percent) in {20, 40, 60, 80, 99}:
            cue = f"voice_{int(percent)}"
            self.play_one_shot(cue)

    def finish_session(self, success: bool):
        self.osc.send_message("/finish", 1.0 if success else 0.0)

    def play_one_shot(self, cue: str, custom_file: str | None = None):
        if cue.startswith("voice_"):
            file = self.samples_path / f"{cue}.wav"
            if file.exists():
                self.osc.send_message("/play_sample", str(file))
            else:
                log.debug("Sample not found: %s", file)
        elif cue == "ding":
            self.osc.send_message("/ding", 1.0)
        elif cue == "custom" and custom_file:
            self.osc.send_message("/play_sample", custom_file)
        else:
            log.debug("Unknown one-shot cue: %s", cue)