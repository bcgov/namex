function Get-MoveGsDllString($toolsPath) {
#Note the exit 0 - we want this to succeed no matter
"
PowerShell -NoProfile -ExecutionPolicy Bypass -Command `"ls '`$(SolutionDir)\packages\GhostScriptSharp.*\Tools\gsdll32.dll' | Sort -Descending | Select -First 1 | cp -Destination '`$(TargetDir)'; exit 0`""
}