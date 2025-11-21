Pure Data Patch — orchestra.pd
This file will contain the complete .pd patch source (text format) once we orchestrate it.
Requirements for the final patch:

Receive OSC on port 4559
Addresses: /progress <0-100>, /finish <0/1>, /play_sample , /ding, /tada
Implement exact progression from music-design.md
Warm analog-style sound (lop~ filters, light reverb)
Sample player for voice cues
Auto-generate if missing (see src/pd_orchestra.py)

We will generate the full patch in a dedicated goal session after the Python server is stable.


Add tmp to .gitignore (recommended)
"If tmp folder exists, ignore everything inside" | Out-File -Encoding utf8 ".gitignore" -Append
"lode/tmp/" | Out-File -Encoding utf8 ".gitignore" -Append
Write-Host "Lode files created successfully!" -ForegroundColor Green
Write-Host "Next step: seed your agent with these files and start Goal 1 (MCP skeleton)."