# DSH 插件清单（迁移用）

> 导出时间：2026-10-12。插件全部来自 DSH 插件市场 / npm，**不需要上传二进制**，新机器上按名称重装即可。
> 本清单即「列出名称」的交付物；版本号以导出时为准，重装时默认装最新版即可。

## Desktop profile（桌面主 profile，11 个）

| 插件包名 | 导出时版本 | 用途 |
|---|---|---|
| @dsh-market/plugin | ^0.4.11 | 插件市场本体（DSH 自带/先装它） |
| @eddyskywalker/dsh-chatgpt-subscription | ^0.15.0 | ChatGPT 订阅渠道（模型/图像走订阅账号） |
| @linxin666/dsh-web-all | ^0.4.5 | Web 界面套件（桌宠、皮肤中心等） |
| @liustack/modsearch | 5.10.6 | 搜索桥（read_page / x_search 等） |
| dsh-context | ^0.65.0 | 上下文增强 |
| dsh-free-search | ^0.8.2 | 自由搜索（多引擎并发） |
| dsh-image-gen | ^0.8.7 | 图像生成/编辑工具 |
| dsh-mnemon | ^0.5.25 | 记忆系统（含 memory-spaces/documents 等 16 个子件） |
| dsh-plugin-wallpaper-engine | ^1.3.1 | 壁纸引擎 |
| dsh-vision-router | ^3.0.3 | 视觉路由（截图/OCR/像素对比等） |
| proposal-generator-cn | link:本地 | 项目书生成插件，源码在 GitHub: ccccty/proposal-generator-cn |

## Web profile（1 个）

| 插件包名 | 导出时版本 | 用途 |
|---|---|---|
| @wxg-prc-cpg/browser-skill-dsh-plugin | ^0.3.2 | 浏览器自动化 skill 插件 |

## 重装方法

新机器上打开 DSH → 插件市场，按上表名称逐个搜索安装即可。
proposal-generator-cn 用「从 GitHub 安装」或克隆后 link：
```
git clone git@github.com:ccccty/proposal-generator-cn.git
# 在 DSH 插件设置里添加本地路径，或按插件 README 操作
```

## 个性化配置

插件装完后，把 `config/` 里两个文件覆盖到对应位置即可恢复全部个人设置
（模型渠道、生图配置、权限预设、主题、语言等）：

- `config/desktop-cordis.patch.yml` → `~/.dsh/profiles/desktop/cordis.patch.yml`
- `config/web-cordis.patch.yml` → `~/.dsh/profiles/web/cordis.patch.yml`
