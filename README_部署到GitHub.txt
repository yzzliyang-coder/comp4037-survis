COMP4037 作业 3 — SurVis 你已具备本地数据

本地预览（先确认可用再上传）
---------------------------------
用 Chrome/Edge 打开（路径按你本机为准）：
  ...\4037Research Methods\SurVis\src\index.html

应看到 11 条：10 篇课程文献 + 1 篇 SurVis 工具论文（Beck 等）。截图时可在 SurVis 里用关键词筛掉 tool:SurVis，只显示 10 篇亦可。

已替你完成的操作
---------------------------------
- bib/references.bib 已写入 10 篇 DOI 文献 + Beck2016Visual
- 已运行一次数据生成：src/data/generated/bib.js 等已更新
- src/properties.js：editable=false；标题与页脚说明已改成课程相关

发布 GitHub Pages（得到作业要的 live URL）
---------------------------------
1. 在 GitHub 新建仓库，例如 comp4037-survis（名称随意）。
2. 把整个 SurVis 文件夹里的内容推到仓库根目录（含 bib、src 等）。
3. 仓库 Settings → Pages → Branch选 main，Folder选 / (root) → Save。
4. 几分钟后站点类似：https://你的用户名.github.io/comp4037-survis/
5. SurVis 入口通常是：https://你的用户名.github.io/comp4037-survis/src/
   在浏览器打开确认能显示文献，再把该完整 URL 写进报告图注。

若你之后修改 references.bib，在 SurVis 根目录执行：
  python -c "code=open('update_data.py',encoding='utf-8').read(); exec(code.split('prevBibTime = 0')[0]); update()"

（比一直运行 update_data.py 更方便，避免死循环。）
