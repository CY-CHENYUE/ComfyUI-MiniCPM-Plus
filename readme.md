# MiniCPM-Plus

这个自定义节点包为 ComfyUI 添加了 MiniCPM 语言模型,实现了高级文本生成和图像理解功能。

## 与Flux配合使用
![image](https://github.com/user-attachments/assets/0979f795-cfa1-49e0-a4c2-4faabfe15ced)


## 描述图像
### 提示词反推与短标签
![image](https://github.com/user-attachments/assets/c707e6b8-02b4-4e44-a657-ef6c58c09d96)

## 文本生成
![image](https://github.com/user-attachments/assets/eaa09585-0ff4-4f2b-8adb-dffe6835e216)



## 功能

- **MiniCPM-Plus: 3-4B**: 强大的文本生成语言模型。
- **MiniCPM-Plus: V-2.6**: 先进的视觉-语言模型,能够理解和描述图像。
- **MiniCPM-Plus: TextDisplay**: 在 ComfyUI 中显示生成文本的实用节点。

## 安装方法

### 方法1: 使用 ComfyUI-Manager

1. 确保你已经安装了 [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)。
2. 在 ComfyUI 界面中,打开 "Manager" 选项卡。
3. 在搜索框中输入 "MiniCPM-Plus"。
4. 找到 "MiniCPM-Plus" 并点击 "Install" 按钮。
5. 安装完成后,重启 ComfyUI。

### 方法2: 手动安装

1. 进入您的 ComfyUI 自定义节点目录:
   ```
   cd ComfyUI/custom_nodes/
   ```

2. 克隆此仓库:
   ```
   git clone https://github.com/CY-CHENYUE/Comfyui-MiniCPM-Plus.git
   ```

3. 重启 ComfyUI。

所需的依赖项将在首次使用时自动安装。

## 使用方法

安装后,新节点将出现在节点菜单的 "MiniCPM-Plus" 类别下。

### MiniCPM-Plus: 3-4B

用于文本生成任务。连接字符串输入来基于提示生成文本。

### MiniCPM-Plus: V-2.6

此节点可以处理文本和图像。连接图像输入和文本提示来生成描述或回答关于图像的问题。

### MiniCPM-Plus: TextDisplay

使用此实用节点在 ComfyUI 工作流中显示 MiniCPM 节点的输出文本。

## 参数说明

- **max_new_tokens**: 生成的最大标记数 (默认: 300)。
- **temperature**: 控制生成的随机性 (默认: 0.5)。
- **top_p**: 核采样参数 (默认: 0.8)。
- **top_k**: Top-k 采样参数 (默认: 50)。
- **seed**: 用于可重现性的随机种子 (默认: 0)。
- **extract_keywords**: (仅适用于 MiniCPM-Plus: V-2.6) 是否从生成的文本中提取关键词 (默认: False)。

## 注意事项

- 模型将在首次使用时自动下载。这可能需要一些时间,具体取决于您的网络连接。
- 所需的依赖项将在首次使用时自动安装。如果安装失败,请查看控制台输出并手动安装缺失的包。


## 许可证

本项目采用 Apache 许可证 2.0。详情请见 [LICENSE](LICENSE) 文件。

## 致谢

本项目使用了由 [OpenBMB](https://github.com/OpenBMB) 开发的 MiniCPM 模型。
