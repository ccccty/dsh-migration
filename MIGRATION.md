# DSH 迁移指南（旧机 → 新机）

## 包里有什么

| 内容 | 位置 | 迁移方式 |
|---|---|---|
| 插件清单（11+1 个） | plugins/PLUGINS.md | 市场按名重装，不用上传 |
| 个性化配置（模型/生图/权限/主题） | config/*.yml | 覆盖到 ~/.dsh/profiles/ |
| 自建技能 paper-generation-cn | skills/paper-generation-cn | 拷到 ~/.dsh/skills/ |
| 第三方技能 find-skills、draw-io-diagram-generator | skills/ | 拷到对应目录（见下） |
| 旧版军工项目书技能（已被 proposal-generator-cn 取代，存档用） | legacy/ | 可不装 |
| 一键恢复脚本 | install.ps1 | 新机 PowerShell 执行 |

不在包里的：
- **proposal-generator-cn**（自建主技能+插件）：在独立仓库 ccccty/proposal-generator-cn，直接 clone
- **ruflo**（134MB）：第三方，新机重装，见 skills/README.md
- **凭据**（绝不入库）：~/.dsh/.credentials.yaml、CCCTY_API_KEY 环境变量、GitHub SSH 私钥 —— 用 U 盘/局域网手动拷

## 新机迁移步骤

1. 装 DSH（新版本自带 marketplace）
2. 装插件：按 plugins/PLUGINS.md 清单在市场逐个安装
3. 跑 install.ps1（恢复技能 + 配置），或手动：
   - skills/paper-generation-cn、find-skills → C:\Users\<你>\.dsh\skills\
   - skills/draw-io-diagram-generator → C:\Users\<你>\.agents\skills\
   - config 两个 yml → ~/.dsh/profiles/ 对应覆盖
   - git clone 主技能仓库，把 skills/proposal-generator-cn 拷到 ~/.dsh/skills/
4. 手动恢复凭据：.credentials.yaml、环境变量 CCCTY_API_KEY、~/.ssh 私钥
5. 工具链按需重装到 D 盘：drawio、MinGit、tectonic、miniconda、VS Code（清单见 legacy 记忆或旧机 D:\devtools）

## 验证

新机开 DSH 新会话，说「列出可用技能」应看到：proposal-generator-cn、paper-generation-cn、
find-skills、draw-io-diagram-generator（+内置 office 三件套等）。生图/搜索/视觉工具各试一次。
