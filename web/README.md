# 网页版（移动端适配）

> 本目录是**网页版**：根目录 `main.py` 的独立副本 + 触屏适配 + pygbag 打包入口。
> 根目录的桌面版**不受影响**，命令仍是 `python main.py`。
> 打包与分享步骤见本文，**不改动 `docs/` 下的任何设计文档**。

## 1. 与桌面版的差别

| 项 | 桌面版（根目录） | 网页版（本目录） |
| --- | --- | --- |
| 入口 | `main.py` | `web/main.py` |
| 主循环 | `while True` + `clock.tick(60)` | `async def main()` + 每帧 `await asyncio.sleep(0)`（pygbag 要求让出控制权） |
| 输入 | 鼠标左键、空格/回车、ESC、滚轮 | 同左，另加**触屏轻触**与**滑动手势** |
| 点击判定 | `hit()` 按基准矩形 | `hit()` 在有手指输入时把命中区向外**放大 12 基准像素** |
| 资源 | `game/`、`data/`、`fonts/`、`audio/` | 本目录内的**副本** |
| 存档 | `save/records.json`（保留你的记录） | `web/save/records.json`（空存档，随包分发） |

## 2. 触屏与手势

| 手势 | 位置 | 行为 |
| --- | --- | --- |
| 轻触 | 任意按钮 | 等价鼠标左键（命中区自动放大，按不准也能点到） |
| 上下滑 | 游戏主界面 | 滚动月度日志（上滑看更早的月份；手动滚动后停止自动跟随） |
| 上下滑 | 成就页 / 回顾页 / 回顾详情 | 滚动列表 |
| 左滑 | 游戏主界面 | 推进一个月（等价点「继  续」） |
| 右滑 | 游戏主界面 | 打开暂停页 |
| 右滑 | 暂停 / 结局 / 成就 / 回顾 / 回顾详情 | 返回上一页（等价点「返回首页」或「返  回」） |

- 滑动阈值 **40 基准像素**：位移小于它算轻触、大于它算滑动
- 响应式沿用桌面版规则：基准画幅 540 × 960，缩放系数取 `min(宽/540, 高/960)` 并居中留白 —— 手机竖屏、横屏、平板都能完整显示

## 3. 本地运行（桌面窗口）

    cd web
    python main.py

## 4. 打包成网页版（pygbag）

先装依赖（pygbag 只用于打包，桌面版不需要）：

    pip install -r requirements.txt

**方式一：开发服务器（推荐，Codespaces 里就用这个）**

    pygbag web

浏览器打开 http://localhost:8000 即可；服务器会自己把 Python 编译成 WebAssembly。

**方式二：构建静态站点**

    pygbag --build web
    python -m http.server -d web/build/web 8000

产物在 `web/build/web/`，可整目录上传到任意静态托管。

## 5. GitHub Codespaces 分享步骤

1. 把仓库推到 GitHub（`main` 分支）
2. 打开仓库页 → **Code ▾ → Codespaces → Create codespace on main**
3. 等容器就绪：`.devcontainer/devcontainer.json` 会自动执行 `pip install -r requirements.txt`
4. 在终端里运行 **`pygbag web`**
5. 左侧 **Ports** 面板找到 **8000** → 右键 → **Port Visibility → Public**
6. 复制该端口的转发地址（形如 `https://xxx-8000.app.github.dev/`）发给别人，手机浏览器也能直接玩

> 停止 Codespace 后转发链接会失效；重新启动后在同一个端口重启 `pygbag web` 即可继续分享（免费额度用完后 Codespace 会自动休眠）。

## 6. 注意事项

- **浏览器里没有持久存档**：网页版的 `save/records.json` 与 `exports/` 写在 WASM 虚拟文件系统里，刷新页面即恢复初始状态（这是浏览器沙箱的限制，不是 bug）
- **音效需要先有一次点击**：浏览器要求用户交互后才允许播放声音，第一次点击之后按钮音效才会响
- **同步提醒**：本目录是副本，改完根目录的 `main.py` / `game/` / `data/` 后要同步过来，例如

      Copy-Item main.py web\main.py -Force
      Copy-Item game,data,fonts,audio -Destination web -Recurse -Force

  （同步 `main.py` 后，`web/main.py` 里的 async 主循环、触屏与手势代码需要重新加回 —— 见本文 §1 的差异表）

## 7. Codespaces 启动太慢怎么办

启动耗时几乎全在容器侧，与游戏代码无关（本仓库 90 个文件 / 9.7 MB）。按**收益从大到小**处理：

| 序号 | 做法 | 位置 | 预计效果 |
| --- | --- | --- | --- |
| 1 | **配置 Prebuild（预构建）** | 仓库 Settings → Codespaces → Prebuilds → 新建，分支选 `main` | 新建 Codespace 从数分钟降到 **十几秒**（预构建会把镜像、依赖、扩展全部提前装好） |
| 2 | **延长闲置超时** | 仓库 Settings → Codespaces → Idle timeout 调到 **240 分钟** | 避免频繁冷启动；已停止的 Codespace 点 **Resume** 比新建快得多 |
| 3 | 依赖安装放在 `onCreateCommand` | 已改好（`.devcontainer/devcontainer.json`） | `postCreateCommand` **不会被预构建缓存**，`onCreateCommand` 才会；这一步改完，预构建才真正有效 |
| 4 | 去掉 VS Code 扩展自动安装 | 已改好（移除了 `ms-python.python`） | 省掉约 100 MB 扩展下载；需要时在 Codespaces 里自己装即可 |
| 5 | 关闭端口自动预览 | 已改好（`onAutoForward` 改为 `notify`） | 启动时不再额外加载一次预览页 |
| 6 | 机器类型 | 新建 Codespace 时选 **4-core** | 依赖安装阶段更快（免费额度消耗也更快，按需选） |
| 7 | 网络 | 本地网络 | 国内直连 Codespaces 前端（`*.app.github.dev`、`vscode-cdn.net`）经常很慢，这一步只能靠代理解决 |

### 更省事的路子：静态托管（推荐给"只想给别人玩"的场景）

Codespaces 是**开发环境**，不是托管服务 —— 每次分享都要等它启动。若只是想给同学/老师一个试玩链接，把 pygbag 的静态产物丢到静态托管更合适：

    pygbag --build web          # 产物在 web/build/web/
    # 再把 web/build/web/ 整目录发布到 GitHub Pages / Cloudflare Pages

- 打开即玩，首屏只需拉一次 WASM 运行时
- 不占用 Codespaces 额度，也不会因为闲置而失效
- 首次打开想更快，可用 `pygbag --archive web`（把资源打成单个归档，减少请求数）

> 注意：网页版首屏要下载 `fonts/zpix.ttf`（**4.7 MB**，仅用于首页大标题）与 CPython 的 WASM 运行时，手机首次打开会慢几十秒；想进一步提速，可以给网页版改用系统字体、去掉这个 4.7 MB 资源（属于视觉设计变更，需人类定夺）。