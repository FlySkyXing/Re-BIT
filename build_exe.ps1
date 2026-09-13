# 打包成 Windows exe（PyInstaller --onedir，资源放在 exe 旁边）
#
# 用法：powershell -ExecutionPolicy Bypass -File build_exe.ps1
#       powershell -ExecutionPolicy Bypass -File build_exe.ps1 -SkipTest   （跳过启动自检）
#
# 说明：exe 用相对路径读 data/ fonts/ audio/，所以资源不打进 exe、直接放在同目录，
#       好处是无需改动任何游戏代码；交付时把 dist\<名称> 整个目录压成 zip 即可。

param(
    [string]$Name = "BIT重开模拟器",
    [switch]$SkipTest
)

Set-Location $PSScriptRoot
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

python -c "import importlib.util as u; raise SystemExit(0 if u.find_spec('PyInstaller') else 1)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "未安装 PyInstaller，请先执行： python -m pip install pyinstaller" -ForegroundColor Yellow
    exit 1
}

Write-Host "正在清理旧的打包产物 …" -ForegroundColor Cyan
Remove-Item build,dist,"$Name.spec" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "正在打包（首次约 1~3 分钟）…" -ForegroundColor Cyan
python -m PyInstaller --noconfirm --clean --onedir --noconsole --name $Name main.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "打包失败，请看上面的报错" -ForegroundColor Red
    exit $LASTEXITCODE
}

$out = Join-Path $PSScriptRoot "dist\$Name"
Write-Host "正在把运行期资源放到 exe 旁边 …" -ForegroundColor Cyan
Copy-Item data,fonts,audio -Destination $out -Recurse -Force
New-Item -ItemType Directory -Force "$out\save","$out\exports" | Out-Null

# 交付用空存档（不带开发机上的个人记录）；必须写成不带 BOM 的 UTF-8，否则 json.load 会报错
$recordsLines = @('{', '  "achievements": [],', '  "games": [],', '  "provinces": []', '}')
$recordsText = ($recordsLines -join "`r`n") + "`r`n"
[System.IO.File]::WriteAllText("$out\save\records.json", $recordsText, (New-Object System.Text.UTF8Encoding($false)))

$exe = Join-Path $out "$Name.exe"
if (-not (Test-Path $exe)) {
    Write-Host "打包结束但找不到 exe：$exe" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "产物目录：$out" -ForegroundColor Green
Get-ChildItem $out | Select-Object Name,Length | Format-Table -AutoSize

if (-not $SkipTest) {
    Write-Host "启动自检（用 dummy 视频驱动跑 3 秒，确认不是一启动就崩）…" -ForegroundColor Cyan
    $env:SDL_VIDEODRIVER = "dummy"
    $env:SDL_AUDIODRIVER = "dummy"
    $proc = Start-Process -FilePath $exe -PassThru
    Start-Sleep -Seconds 3
    if ($proc.HasExited) {
        Write-Host "启动自检失败：进程 3 秒内退出（退出码 $($proc.ExitCode)）" -ForegroundColor Red
    } else {
        Write-Host "启动自检通过：进程正常运行" -ForegroundColor Green
        $proc.Kill()
    }
    Remove-Item Env:SDL_VIDEODRIVER,Env:SDL_AUDIODRIVER -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "交付方式：把整个目录压成 zip 发给别人，解压后双击 exe 即可游玩" -ForegroundColor Green
Write-Host "（存档在 exe 同目录的 save\records.json，导出在 exports\）"
