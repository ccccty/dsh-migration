# 01 · 本地 LaTeX 工具链（本机实测事实）

## 工具布局（全在 D 盘）

| 组件 | 位置 | 备注 |
|---|---|---|
| Tectonic 0.17 | `D:\devtools\tectonic\tectonic.exe` | XeTeX 内核，自包含；支持 `--synctex`、`--keep-logs`；**无 `--watch`，无 biber** |
| Tectonic 缓存 | `D:\devtools\tectonic\cache` | 用环境变量 `TECTONIC_CACHE_DIR` 指定，避免落到 C 盘 |
| Noto CJK 字体 | 主档 `D:\devtools\fonts`；已做**当前用户级安装**（`%LOCALAPPDATA%\Microsoft\Windows\Fonts` + HKCU 注册表） | fontspec 可按名字 `Noto Serif CJK SC` 直接解析，**无需任何环境变量** |
| VS Code 1.141 便携版 | `D:\devtools\vscode` | **版本化布局**：负载在 `<commit>\` 子目录，根目录只有 `Code.exe` 和 `bin\code.cmd`，**切勿拍平** |
| LaTeX Workshop 10.19.0 | `D:\devtools\vscode\data\extensions\` | 解包 VSIX 安装；另有用户自装的 tomoki1207.pdf 与中文语言包 |
| TeX 命令 shim | `D:\devtools\texbin\` | `xelatex/latexmk/pdflatex/lualatex.cmd` 全部转发到 Tectonic（取最后一个参数为文档，无 .tex 自动补）；已加入用户 PATH |
| 论文工作区 | `D:\devtools\paper.code-workspace` | 打开即带正确配置 |
| 启动器 | `D:\devtools\paper-editor.cmd`（桌面有快捷方式「论文编辑 (VS Code)」） | 内含清 `ELECTRON_RUN_AS_NODE` 和 PATH 注入 |
| Miniconda / Python | `D:\devtools\miniconda3\python.exe` | pymupdf 已装，用于 PDF 验证 |

## 编译配方（实测通过）

```powershell
Set-Location <论文目录>            # 先 cd，之后全部用相对路径
$env:TECTONIC_CACHE_DIR="D:\devtools\tectonic\cache"
& D:\devtools\tectonic\tectonic.exe -X compile --synctex --keep-logs main.tex
```

验证编译质量的命令见 `tools\build_paper.py`。

## Tectonic 的能力边界

- **没有 biber/bibtex 工作流**：参考文献用 `thebibliography` 内联。若未来模板必须 biblatex/biber，升级路径是 MiKTeX（可装 D 盘，约 250MB）。
- **不自动补 .tex 扩展名**：`tectonic main` 会报 `failed to open input file "main"`，必须给 `main.tex`。
- 网络可用时会自动下载缺失的 .pfb 字体等，属正常现象。

## VS Code 侧配置要点（已配好，勿乱动）

- recipe 工具参数必须用 `%DOC_EXT%`（带扩展名），**不能用 `%DOC%`**（不带扩展名，Tectonic 打不开）。
- `latex-workshop.latex.build.enableMagicComments: false`——否则 main.tex 首行 `% !TeX program = xelatex` 会让插件去 spawn xelatex（实测 forceRecipeUsage 拦不住，原因未查明；shim 层兜底）。
- `recipe.default` 按名字锁定 `"Tectonic"`，不要 `"first"`。
- 快捷键（光标必须在 LaTeX 编辑器内才生效）：编译 `Ctrl+Alt+B`、看 PDF `Ctrl+Alt+V`、正反向 SyncTeX `Ctrl+Alt+J` / PDF 里 Ctrl+点击。
- **改了配置文件后要「重新加载窗口」或完全重启 VS Code 才生效**。

## DSH pwsh 环境的坑（调用工具时必记）

1. **ELECTRON_RUN_AS_NODE=1 泄漏**：DSH 是 Electron 应用，从 pwsh 里启动任何 Electron 程序（VS Code）都会退化成裸 Node 报 "Cannot find module"。启动前必须 `Remove-Item Env:\ELECTRON_RUN_AS_NODE` 或在 cmd 里 `set ELECTRON_RUN_AS_NODE=`。
2. **PS 5.1 传非 ASCII 参数给原生命令会被 GBK 重编码损坏**：`Start-Process`/调用 .exe 传中文路径参数必坏。对策：中文路径放进 UTF-8 配置文件，命令行只传 ASCII；或先 `Set-Location` 进目录再用相对路径（Set-Location 走 PowerShell 内部字符串，不受影响）。
3. **PS 5.1 `Get-Content` 读 UTF-8 无 BOM 文件按 GBK 误解码**：会制造"JSON 坏了"假象（GBK 尾字节吃掉结尾引号）。验证 UTF-8 文件用 read 工具或 Python，别用 Get-Content|ConvertFrom-Json。
4. Windows 下被强杀的进程退出码是 1 且无信号标记——裸 exit 1 先当中断看待，别当命令失败。
5. `read` 工具对长行 Markdown 可能静默丢行，验收文件完整性用 pwsh `Get-Content -Raw` 按字节核验。
