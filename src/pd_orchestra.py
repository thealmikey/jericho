# src/pd_orchestra.py
import subprocess
import time
import os
from pythonosc import udp_client
from pathlib import Path

class PdOrchestra:
    def __init__(self):
        self.pd_process = None
        self.osc = udp_client.SimpleUDPClient("127.0.0.1", 4559)  # Pd receives on 4559
        self.patch_path = Path(__file__).parent.parent / "pd" / "orchestra.pd"
        self.samples_path = Path(__file__).parent.parent / "samples"
        self.start_pd()

    def start_pd(self):
        if not self.patch_path.exists():
            self.generate_patch()
        self.pd_process = subprocess.Popen([
            "pd", "-nogui", "-audiodev", "1,2", "-open", str(self.patch_path)
        ])
        time.sleep(1.5)  # give Pd time to boot

    def generate_patch(self):
        # Tiny procedural patch – chords + arpeggio + sample player
        pd_content = """
#N canvas 0 0 800 600 10;
#X obj 0 0 inlet;
#X obj 0 50 route /progress /finish /oneshot;
#X obj 100 100 osc_receive 4559;
#X connect 0 0 2 0;

#X obj 150 150 lop~ 0.1;  # gentle low-pass for warmth
#X obj 150 200 dac~;

#X obj 200 150 nbx 0-100;  # current progress
#X obj 250 150 *~ 0.01;    # scale to control density/speed

#X coords ... (abbreviated – full patch below in lode/pd-patch.md)
        """
        # In real session ask the agent to write the full .pd file with:
        # - metro whose speed = progress
        # - chord progression (C Eb G Bb → F G C E etc.)
        # - rising arpeggiator
        # - trigger sample player on milestones
        self.patch_path.parent.mkdir(parents=True, exist_ok=True)
        # We'll let the agent write the full beautiful patch in the next goal

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
        elif cue == "ding":
            self.osc.send_message("/ding", 1.0)
        # etc.