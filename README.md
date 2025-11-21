# Sound Orchestra MCP

Lightweight MCP server that turns progress updates into a friendly Pure Data soundtrack.

Quick start

1. Install Python deps:

```powershell
pip install -r requirements.txt
```

2. Install Pure Data (pd) and ensure `pd` is on your PATH.
   - This patch uses the `mrpeach` Pd externals for OSC parsing. Install `mrpeach` (Pd package manager) or ensure `oscparse` / `routeOSC` are available in your Pd installation.

3. Run the server (from repo root):

```powershell
python src/main.py
# or
python -m uvicorn src.main:app --reload --port 2424
```

Notes
- Pd must accept OSC on port `4559` (the Python server sends messages to `127.0.0.1:4559`).
- Voice/sample files should go in the `samples/` directory (e.g. `samples/voice_20.wav`). The server passes absolute paths to Pd when triggering samples.
- `lode/music-design.md` is the authoritative spec for how music evolves with progress; do not change it without explicit intent.

Files of interest
- `manifest.json` — tool definitions and schemas exposed by the MCP.
- `src/main.py` — FastAPI endpoints and single global `PdOrchestra` instance.
- `src/pd_orchestra.py` — OSC client and Pd subprocess launcher; will open `pd/orchestra.pd`.
- `pd/orchestra.pd` — Pure Data patch that receives OSC and generates audio.

If you want, I can also:
- Implement additional Pd externals installation instructions for your platform.
- Generate example sample `.wav` files or wire up a small TTS script to produce `samples/voice_*.wav` cues.

Verifier CLI
------------

Run the friendly verifier to exercise the OSC endpoints and (optionally) start Pd. It will send a few `/progress` updates and one-shot cues so you can confirm audio behavior.

```powershell
python src/verify.py
python src/verify.py --no-pd
python src/verify.py --pd "C:\\Program Files\\Pd\\pd.exe"
```

If Pd is available and the patch is loaded, you should hear gentle test notes and cues during the run.
