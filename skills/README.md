# Skills 迁移说明

| skill | 类型 | 安装位置 | 方式 |
|---|---|---|---|
| paper-generation-cn | 自建（LaTeX 中文论文） | ~/.dsh/skills/ | 本目录直接拷 |
| find-skills | 第三方（skills CLI 配套） | ~/.dsh/skills/ | 本目录直接拷 |
| draw-io-diagram-generator | 第三方（awesome-copilot） | ~/.agents/skills/ | 本目录直接拷，或 `pnpm dlx skills add github/awesome-copilot@draw-io-diagram-generator` |
| proposal-generator-cn | 自建主技能 | ~/.dsh/skills/ | git clone ccccty/proposal-generator-cn 后拷 skills/ 子目录 |
| ruflo | 第三方（134MB，未收录） | ~/.dsh/skills/ | 按 ruflo 官方文档重装（npm 生态） |
