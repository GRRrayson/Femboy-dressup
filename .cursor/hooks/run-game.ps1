$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $projectRoot

$pythonCmd = Get-Command py -ErrorAction SilentlyContinue
if ($pythonCmd) {
    Start-Process -FilePath "py" -ArgumentList "game.py" -WorkingDirectory $projectRoot
    exit 0
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    Start-Process -FilePath "python" -ArgumentList "game.py" -WorkingDirectory $projectRoot
    exit 0
}

Write-Output '{"permission":"allow"}'
exit 0
