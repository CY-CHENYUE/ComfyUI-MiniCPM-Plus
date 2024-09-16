# MiniCPM-Plus

## 功能

在ComfyUI里使用MiniCPM做提示词反推与提示词生成。

### 1. MiniCPM3-4B 和 MiniCPM3-4B-GPTQ-Int4

这两个节点都专注于文本生成任务，但针对不同的硬件需求进行了优化。

- **功能**：
  - 高质量文本生成
  - 提示词生成
- **特点**：
  - 支持长文本生成
  - 适用于各种文本生成任务

#### MiniCPM3-4B
- 提供完整的模型性能
- 适合有足够显存的设备

#### MiniCPM3-4B-GPTQ-Int4
- 使用 GPTQ 量化技术，大幅降低内存占用
- 保持与原始模型相近的性能
- 适用于资源受限的环境

### 例子
#### 提示词生成
![image](https://github.com/user-attachments/assets/28bb9b51-d8b0-49ed-ba43-d51e1d65bd0a)

#### 生成提示词用于Flux出图
![image](https://github.com/user-attachments/assets/e6cbc806-4701-4fdc-8105-219afcc4eb40)


### 2. MiniCPM-V-2.6 和 MiniCPM-V-2.6-INT4

这两个节点都是视觉-语言模型，能够处理图像和文本的多模态任务。

- **功能**：
  - 图像描述
  - 提示词反推
  - 图像内容识别
  - 关键词提取
- **特点**：
  - 支持图像输入
  - 可以生成图像相关的文本描述和提示词
  - 提供关键词提取功能

#### MiniCPM-V-2.6
- 完整的视觉-语言模型，提供最佳性能
- 适合有高性能GPU的设备

#### MiniCPM-V-2.6-INT4
- INT4 量化版本，显存占用更低（约 7GB）
- 保持与原始 MiniCPM-V-2.6 相同的功能
- 适用于中端显卡和资源受限的环境

### 例子
#### 图片提示词反推长文本描述+短标签
![image](https://github.com/user-attachments/assets/a5ae7944-d7a6-4ef4-9818-aa4103a9f723)

#### 图片提示词反推用于Flux出图
![image](https://github.com/user-attachments/assets/783ed50d-e4a6-423e-8cd3-c94e525c5dfa)



## 使用说明

1. 在 ComfyUI 中，可以找到这四个新的节点：`MiniCPM3-4B`、`MiniCPM3-4B-GPTQ-Int4`、`MiniCPM-V-2.6` 和 `MiniCPM-V-2.6-INT4`。
2. 对于文本生成任务：
   - 如果足够的显存，使用 `MiniCPM3-4B` 节点以获得最佳性能。
   - 如果显存有限，使用 `MiniCPM3-4B-GPTQ-Int4` 节点以在性能和资源使用之间取得平衡。
3. 对于图像相关任务：
   - 如果高性能GPU，使用 `MiniCPM-V-2.6` 节点以获得最佳效果。
   - 如果使用中端显卡或资源受限，选择 `MiniCPM-V-2.6-INT4` 节点。
4. 所有节点都支持自定义参数，如 max_new_tokens、temperature、top_p 和 top_k。
5. 视觉模型节点还支持关键词提取功能，可以通过 `extract_keywords` 参数启用。

## 注意事项

- 首次使用时，节点会自动下载所需的模型文件，请确保网络连接正常。
- 量化模型（GPTQ-Int4 和 INT4 版本）需要更少的显存，适合资源受限的环境，但可能会有轻微的性能损失。
- 所有模型都支持中英双语输入和输出。

## 安装方法

### 方法1: 使用 ComfyUI-Manager

1. 确保已经安装了 [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)。
2. 在 ComfyUI 界面中,打开 "Manager" 选项卡。
3. 在搜索框中输入 "MiniCPM-Plus"。
4. 找到 "MiniCPM-Plus" 并点击 "Install" 按钮。
5. 安装完成后,重启 ComfyUI。

### 方法2: 手动安装

1. 进入 ComfyUI 自定义节点目录:
   ```
   cd ComfyUI/custom_nodes/
   ```

2. 克隆此仓库:
   ```
   git clone https://github.com/CY-CHENYUE/Comfyui-MiniCPM-Plus.git
   ```

3. 重启 ComfyUI。

所需的依赖项将在首次使用时自动安装。


## 许可证

本项目采用 Apache 许可证 2.0。详情请见 [LICENSE](LICENSE) 文件。

## 致谢

本项目使用了由 [OpenBMB](https://github.com/OpenBMB) 开发的 MiniCPM 模型。






