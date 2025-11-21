# Suggested Voice Cue Scripts

Use macOS `say`, ElevenLabs, or record yourself:

```powershell
# macOS example
mkdir samples
say -v Daniel -o samples/voice_20.aiff "Twenty percent complete"
say -v Serena -o samples/voice_50.aiff "We're halfway there!"
say -v Daniel -o samples/voice_80.aiff "Almost done"
say -v Serena -o samples/voice_100_success.aiff "All done! Great work!"
say -v Daniel -o samples/voice_100_failure.aiff "Hmm, something went wrong. Let's try again."

Convert .aiff → .wav if needed:
PowerShellGet-ChildItem samples/*.aiff | ForEach-Object { ffmpeg -i $_.FullName ($_.BaseName + '.wav')