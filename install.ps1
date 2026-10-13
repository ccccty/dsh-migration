# DSH 迁移一键恢复脚本（在新机上运行）
# 用法：powershell -ExecutionPolicy Bypass -File install.ps1
$ErrorActionPreference = "Stop"
$pkg = Split-Path -Parent $MyInvocation.MyCommand.Path
$dsh = Join-Path $env:USERPROFILE ".dsh"
$agents = Join-Path $env:USERPROFILE ".agents\skills"

Write-Host "== 1/3 恢复 skills =="
foreach ($s in @("paper-generation-cn", "find-skills")) {
  $dst = Join-Path $dsh "skills\$s"
  Copy-Item -Recurse -Force (Join-Path $pkg "skills\$s") $dst
  Write-Host "  OK: $s -> $dst"
}
New-Item -ItemType Directory -Force $agents | Out-Null
Copy-Item -Recurse -Force (Join-Path $pkg "skills\draw-io-diagram-generator") (Join-Path $agents "draw-io-diagram-generator")
Write-Host "  OK: draw-io-diagram-generator -> $agents"
Write-Host "  提示: proposal-generator-cn 请 git clone git@github.com:ccccty/proposal-generator-cn.git 后把 skills/proposal-generator-cn 拷到 ~/.dsh/skills/"

Write-Host "== 2/3 恢复配置 =="
Copy-Item -Force (Join-Path $pkg "config\desktop-cordis.patch.yml") (Join-Path $dsh "profiles\desktop\cordis.patch.yml")
Copy-Item -Force (Join-Path $pkg "config\web-cordis.patch.yml") (Join-Path $dsh "profiles\web\cordis.patch.yml")
Write-Host "  OK: cordis.patch.yml x2"

Write-Host "== 3/3 手动事项提醒 =="
Write-Host "  - 插件：按 plugins/PLUGINS.md 在市场逐个安装"
Write-Host "  - 凭据：.credentials.yaml / CCCTY_API_KEY 环境变量 / SSH 私钥（用 U 盘拷，不在本包）"
Write-Host "  - 工具链：drawio、MinGit、tectonic 等装到 D 盘"
Write-Host "完成。"
