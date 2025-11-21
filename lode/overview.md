
# Sound Orchestra MCP — Project Overview

**Current date:** November 21, 2025  
**Goal:** A friendly musical progress bar for agentic coding sessions.

This MCP server turns silent, anxiety-inducing agent builds into an audible, evolving soundtrack.  
Instead of staring at a spinner, you hear calm lofi chords that gradually build excitement, add arpeggios, speed up, layer harmony — exactly like a film score that mirrors progress from 0 → 100%.

## Core Idea
- Pure Data (Pd) runs locally as a subprocess.
- The MCP exposes simple tools (`start_progress_music`, `update_progress`, `finish_progress`, `play_one_shot`).
- Music starts calm (intro), density/speed/complexity rise with progress %, ends with triumphant resolve (or sad minor on failure).
- Optional gentle voice cues at milestones (“twenty percent”, “halfway there”, “all done!”).

## Tech Stack
- Python + FastAPI (MCP server)
- python-osc for talking to Pure Data
- Pure Data patch receives OSC on port 4559 and generates all audio
- Optional short .wav voice samples (TTS or recorded)

## Project Structure (Lode Coding native)