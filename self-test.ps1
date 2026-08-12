[CmdletBinding()]
param([ValidateSet('smoke','full')][string]$Suite='smoke',[string]$CaseId='')
$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'
[Console]::OutputEncoding=[Text.UTF8Encoding]::new()
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path; Set-Location $Root
$Venv=Join-Path $Root '.avf\venv'; $Python=Join-Path $Venv 'Scripts\python.exe'
New-Item -ItemType Directory -Force -Path (Join-Path $Root '.avf')|Out-Null
try {
 if(!(Test-Path $Python)){
  if(Get-Command py -ErrorAction SilentlyContinue){& py -3.11 -m venv $Venv}else{& python -m venv $Venv}
 }
 & $Python -m pip install --disable-pip-version-check -e '.[dev]'
 if(Get-Command npm -ErrorAction SilentlyContinue){Push-Location validation; try{& npm install --no-audit --no-fund; & npx playwright install chromium}finally{Pop-Location}}
 $a=@('-m','validation.runner.cli','--suite',$Suite); if($CaseId){$a+=@('--case-id',$CaseId)}
 & $Python @a; exit $LASTEXITCODE
}catch{$_|Out-String|Set-Content -Encoding UTF8 '.avf\bootstrap-failure.txt'; Write-Host $_; exit 40}
