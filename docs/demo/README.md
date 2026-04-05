# skill-hr 演示素材（GIF）

仓库首屏使用的动图为根目录 [`README.md`](../../README.md) 引用的 **`skill-hr-demo.gif`**（与本目录同级）。

## 文件约定

| 文件 | 用途 |
|------|------|
| `skill-hr-demo.gif` | 主演示（建议 20–40 秒循环） |
| `skill-hr-demo.png` | 静态 fallback / 封面；可与 GIF 同画面首帧 |

## 推荐规格

- **画幅**：宽度约 **800–1000 px**（GitHub README 上可读即可）。
- **时长**：**20–40 s**；循环播放时首尾尽量可衔接，或明显「结束→重来」。
- **体积**：目标 **&lt; 5–8 MB**；过大时降低帧率、裁边或缩短时长。
- **隐私**：打码用户名、Token、内网路径、客户名；可用 `~/project` 等占位路径。

## 录制脚本（建议）

1. 打开宿主（Claude Code 或 Cursor），确保已安装 `skill-hr`（见仓库快速上手）。
2. 用户输入一句**真实多步骤任务**（非泛泛聊天）。
3. 镜头包含：agent **先结构化 JD / 匹配思路**（可截取关键段落）。
4. 切到编辑器或文件树：**`.skill-hr/registry.json` 或 `incidents/` 下新文件** 出现或更新的一小段。
5. 结束在「任务已委派或已记录」的稳定画面，便于循环。

## Windows 下制作方式

- **ScreenToGif**：录制 → 编辑删冗余帧 → 导出 GIF，注意帧延迟与压缩。
- **OBS** 录屏 → 用 **ffmpeg** 转 GIF（示例，按路径修改）：

```bash
ffmpeg -i recording.mp4 -vf "fps=10,scale=880:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 skill-hr-demo.gif
```

可先导出短片段试跑参数，再调 `fps` / `scale` 控制体积。

## 替换步骤

1. 将成品保存为 **`docs/demo/skill-hr-demo.gif`**（覆盖占位文件）。
2. 可选：更新 **`skill-hr-demo.png`** 为 GIF 第一帧，便于社交预览或未加载动图时的展示。
3. 本地打开根目录 `README.md` 预览，确认 GitHub 上动图可加载。
