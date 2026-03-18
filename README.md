# 即梦AI视频批量生成工具

批量根据图片生成视频的Python工具，支持多产品目录并发处理。

## 功能特性

- 读取全局配置文件 `config.toml`
- 支持多产品目录，每个产品可独立配置
- 单次并发最多2个视频生成任务
- 支持720P和1080P视频生成
- 自动轮询任务状态
- 生成结果保存为JSON文件

## 目录结构

```
.
├── config.toml                      # 全局配置文件
├── jimeng_video_generator.py        # 主程序
├── requirements.txt                 # Python依赖
├── products/                        # 产品目录
│   ├── product_a/                   # 产品A
│   │   ├── config.toml              # 产品A配置（可选）
│   │   ├── images/                  # 产品A图片目录
│   │   └── videos/                  # 视频输出目录（自动创建）
│   └── product_b/                   # 产品B
│       ├── config.toml              # 产品B配置
│       └── images/                  # 产品B图片目录
└── video_generation_results.json    # 结果文件（自动生成）
```

## 环境要求

- Python 3.8+
- 依赖包：
  - `tomli` - TOML配置文件解析
  - `volcengine` - 火山引擎SDK

安装依赖：
```bash
pip install -r requirements.txt
```

## 配置说明

### 全局配置 (config.toml)

```toml
[default]
# 默认提示词
prompt = "自然流畅的过渡动画"
# 默认生成帧数 (121=5秒, 241=10秒)
frames = 121

[output]
# 图片目录
image_dir = "products"

[api]
# 720P视频req_key
req_key_720p = "jimeng_i2v_first_v30"
# 1080P视频req_key
req_key_1080p = "jimeng_i2v_first_v30_1080"
# 视频质量: 720p 或 1080p
quality = "720p"
```

### 产品配置 (products/产品名/config.toml)

```toml
[product]
# 产品描述（必填）
description = "产品描述信息"
# 独立图片目录（可选，默认使用产品目录本身）
image_dir = "images"

[default]
# 产品特定的提示词（可选）
prompt = "自定义提示词"
# 产品特定的帧数（可选）
frames = 241
```

## 使用方法

### 1. 设置环境变量
> 资源包购买: https://www.volcengine.com/activity/jimeng

> 服务 API 开通: https://console.volcengine.com/ai/ability/detail/2

> 获取密钥地址: https://console.volcengine.com/iam/keymanage


```bash
# Windows
set JIMENG_AK=your_access_key
set JIMENG_SK=your_secret_key

# Linux/Mac
export JIMENG_AK=your_access_key
export JIMENG_SK=your_secret_key
```

### 2. 准备图片

将图片放入产品目录下的 `images` 文件夹（或其他配置的目录），支持格式：jpg、jpeg、png、bmp、webp

### 3. 运行程序

```bash
# 默认运行（最多2并发）
python jimeng_video_generator.py

# 指定并发数
python jimeng_video_generator.py -c 2
```

### 4. 查看结果

程序运行结束后，会在当前目录生成 `video_generation_results.json` 文件，包含所有任务的执行结果。

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-c, --concurrency` | 并发数 | 2 |
| `--config` | 配置文件路径 | config.toml |

## API说明

本工具使用即梦AI视频生成3.0接口：

- 接口地址：`https://visual.volcengineapi.com`
- 提交任务：`Action=CVSync2AsyncSubmitTask`
- 查询任务：`Action=CVSync2AsyncGetResult`

### 视频质量与req_key对应关系

| 质量 | req_key (首帧) |
|------|----------------|
| 720P | jimeng_i2v_first_v30 |
| 1080P | jimeng_i2v_first_v30_1080 |

## 注意事项

1. **图片URL处理**：当前版本需要配置图片服务器URL，或使用支持文件访问的方式
2. **并发限制**：单次并发最多2个任务
3. **任务超时**：单个任务最长等待3分钟
4. **AK/SK安全**：建议使用环境变量方式设置，不要硬编码

## 常见问题

### Q: 如何获取AK/SK？
A: 登录火山引擎控制台，创建访问密钥即可获取。

### Q: 图片需要什么格式？
A: 支持JPEG、PNG、BMP、WebP格式，建议分辨率4096x4096以内。

### Q: 如何修改视频时长？
A: 在配置文件中修改 `frames` 参数：121=5秒，241=10秒。

### Q: 产品目录的图片如何放置？
A: 
- 方式1：直接放在产品目录下（如 `products/product_a/`）
- 方式2：在产品配置中指定 `image_dir = "images"`，放在子目录

## 示例产品配置

### 示例1：产品使用默认配置

```
products/
└── my_product/
    ├── image1.jpg
    └── image2.jpg
```

无需创建 config.toml，将使用全局配置。

### 示例2：产品使用独立配置

```
products/
└── my_product/
    ├── config.toml
    ├── images/
    │   ├── image1.jpg
    │   └── image2.jpg
    └── videos/          # 自动创建
```

config.toml 内容：
```toml
[product]
description = "我的产品描述"
image_dir = "images"

[default]
prompt = "自定义动画描述"
```

## 许可证

MIT License
