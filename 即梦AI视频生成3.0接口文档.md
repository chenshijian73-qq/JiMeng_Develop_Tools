# 即梦AI-视频生成3.0 接口文档

> 即梦视频3.0 —— 即梦同源的文生视频能力，专业级视频生成引擎，释放无限创意。准确遵循复杂指令，视觉表达流畅一致，可驾驭多元艺术风格，在视频生成质量出色的基础上，是**生成效果与速度兼备的高性价比之选。**

本文档整合了720P和1080P视频生成的接口说明，提供了文生视频、图生视频-首帧、图生视频-首尾帧、图生视频-运镜等多种能力。

---

# 目录

- [公共接入说明](#公共接入说明)
  - [请求说明](#请求说明)
  - [通用Query参数](#通用query参数)
  - [通用Header参数](#通用header参数)
  - [通用返回参数](#通用返回参数)
  - [错误码](#错误码)
  - [任务状态说明](#任务状态说明)
  - [AIGCMeta隐式标识配置](#aigcmeta隐式标识配置)
- [720P视频生成](#720p视频生成)
  - [文生视频](#720p文生视频)
  - [图生视频-首帧](#720p图生视频-首帧)
  - [图生视频-首尾帧](#720p图生视频-首尾帧)
  - [图生视频-运镜](#720p图生视频-运镜)
- [1080P视频生成](#1080p视频生成)
  - [文生视频](#1080p文生视频)
  - [图生视频-首帧](#1080p图生视频-首帧)
  - [图生视频-首尾帧](#1080p图生视频-首尾帧)

---

# 公共接入说明

## 请求说明

| 名称 | 内容 |
|------|------|
| 接口地址 | https://visual.volcengineapi.com |
| 请求方式 | POST |
| Content-Type | application/json |

## 通用Query参数

:::tip 拼接到url后的参数，示例：https://visual.volcengineapi.com?Action=CVSync2AsyncSubmitTask&Version=2022-08-31

:::

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| Action | string | 必选 | 接口名，取值：**CVSync2AsyncSubmitTask**（提交任务）或 **CVSync2AsyncGetResult**（查询任务） |
| Version | string | 必选 | 版本号，取值：**2022-08-31** |

## 通用Header参数

:::warning
本服务固定值：**Region为cn-north-1，Service为cv**
:::

主要用于鉴权，详见 [公共参数](https://www.volcengine.com/docs/6369/67268) - 签名参数 - 在Header中的场景部分

## 通用返回参数

请参考[通用返回字段及错误码](https://www.volcengine.com/docs/6444/69728)

### 提交任务返回（通用）

:::tip 重点关注data中以下字段，其他字段为公共返回(可忽略或不做解析)

:::

| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务ID，用于查询结果 |

### 查询任务返回（通用）

:::tip 重点关注data中以下字段，其他字段为公共返回(可忽略或不做解析)

:::

| 参数名 | 类型 | 说明 |
|--------|------|------|
| video_url | string | 生成的视频URL（有效期为 1 小时） |
| aigc_meta_tagged | bool | 隐式标识是否打标成功 |
| status | string | 任务执行状态，详见[任务状态说明](#任务状态说明) |

## 错误码

### 业务错误码

| HttpCode | 错误码 | 错误消息 | 描述 | 是否需要重试 |
|----------|--------|----------|------|--------------|
| 200 | 10000 | 无 | 请求成功 | 不需要 |
| 400 | 50411 | Pre Img Risk Not Pass | 输入图片前审核未通过 | 不需要 |
| 400 | 50511 | Post Img Risk Not Pass | 输出图片后审核未通过 | 可重试 |
| 400 | 50412 | Text Risk Not Pass | 输入文本前审核未通过 | 不需要 |
| 400 | 50512 | Post Text Risk Not Pass | 输出文本后审核未通过 | 不需要 |
| 400 | 50413 | Post Text Risk Not Pass | 输入文本含敏感词、版权词等审核不通过 | 不需要 |
| 400 | 50516 | Post Video Risk Not Pass | 输出视频后审核未通过 | 可重试 |
| 400 | 50517 | Post Audio Risk Not Pass | 输出音频后审核未通过 | 可重试 |
| 400 | 50518 | Pre Img Risk Not Pass: Copyright | 输入版权图前审核未通过 | 不需要 |
| 400 | 50519 | Post Img Risk Not Pass: Copyright | 输出版权图后审核未通过 | 可重试 |
| 400 | 50520 | Risk Internal Error | 审核服务异常 | 不需要 |
| 400 | 50521 | Antidirt Internal Error | 版权词服务异常 | 不需要 |
| 400 | 50522 | Image Copyright Internal Error | 版权图服务异常 | 不需要 |
| 429 | 50429 | Request Has Reached API Limit, Please Try Later | QPS超限 | 可重试 |
| 429 | 50430 | Request Has Reached API Concurrent Limit, Please Try Later | 并发超限 | 可重试 |
| 500 | 50500 | Internal Error | 内部错误 | 可重试 |
| 500 | 50501 | Internal RPC Error | 内部算法错误 | 可重试 |

## 任务状态说明

| 状态值 | 说明 |
|--------|------|
| in_queue | 任务已提交 |
| generating | 任务已被消费，处理中 |
| done | 处理完成，成功或者失败，可根据外层code&message进行判断 |
| not_found | 任务未找到，可能原因是无此任务或任务已过期(12小时) |
| expired | 任务已过期，请尝试重新提交任务请求 |

## AIGCMeta隐式标识配置

依据《人工智能生成合成内容标识办法》&《网络安全技术人工智能生成合成内容标识方法》

在提交任务或查询任务时，可通过`req_json`参数配置隐式标识：

```json
{
  "aigc_meta": {
    "content_producer": "内容生成服务ID",
    "producer_id": "内容生成服务商给此数据的唯一ID",
    "content_propagator": "内容传播服务商ID",
    "propagate_id": "传播服务商给此数据的唯一ID"
  }
}
```

### AIGCMeta 参数说明

| 名称 | 类型 | **可选/必选** | 描述 |
|------|------|--------------|------|
| content_producer | string | 可选 | 内容生成服务ID（长度 <= 256字符） |
| producer_id | string | 必选 | 内容生成服务商给此图片数据的唯一ID（长度 <= 256字符） |
| content_propagator | string | 必选 | 内容传播服务商ID（长度 <= 256字符） |
| propagate_id | string | 可选 | 传播服务商给此图片数据的唯一ID（长度 <= 256字符） |

:::tip 隐式标识验证方式：
https://www.gcmark.com/web/index.html#/mark/check/video

验证步骤：先注册帐号 → 上传打标后的视频 → 点击开始检测 → 输出检测结果即代表成功
:::

---

# 720P视频生成

## 通用参数说明

以下参数适用于所有720P视频生成接口：

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| prompt | string | 必选 | 用于生成视频的提示词，中英文均可输入。建议在400字以内，不超过800字，prompt过长有概率出现效果异常或不生效 |
| seed | int | 可选 | 随机种子，作为确定扩散初始状态的基础，默认-1（随机）。若随机种子为相同正整数且其他参数均一致，则生成视频极大概率效果一致。默认值：-1 |
| frames | int | 可选 | 生成的总帧数（帧数 = 24 * n + 1，其中n为秒数，支持5s、10s）。可选取值：[121, 241]，默认值：121 |

---

## 720P文生视频

### 接口简介

即梦视频3.0文生视频能力，支持720P高清渲染，准确遵循复杂指令，视觉表达流畅一致。

### 提交任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_t2v_v30** |
| prompt | string | 必选 | 用于生成视频的提示词 |
| seed | int | 可选 | 随机种子，默认-1 |
| frames | int | 可选 | 生成的总帧数，默认121（5秒） |
| aspect_ratio | string | 可选 | 生成视频的长宽比。可选取值：["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"]，默认值："16:9" |

#### 请求示例

```json
{
    "req_key": "jimeng_t2v_v30",
    "prompt": "千军万马",
    "seed": -1,
    "frames": 121,
    "aspect_ratio": "16:9"
}
```

#### 返回示例

```json
{
    "code": 10000,
    "data": {
        "task_id": "7392616336519610409"
    },
    "message": "Success",
    "request_id": "20240720103939AF0029465CF6A74E51EC",
    "time_elapsed": "104.852309ms"
}
```

### 查询任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_t2v_v30** |
| task_id | string | 必选 | 任务ID |
| req_json | json string | 可选 | json序列化后的字符串，支持隐式水印配置 |

#### 请求示例

```json
{
    "req_key": "jimeng_t2v_v30",
    "task_id": "7491596536074305586",
    "req_json": "{\"aigc_meta\": {\"content_producer\": \"001191440300192203821610000\", \"producer_id\": \"producer_id_test123\", \"content_propagator\": \"001191440300192203821610000\", \"propagate_id\": \"propagate_id_test123\"}}"
}
```

#### 返回示例

```json
{
    "code": 10000,
    "data": {
        "aigc_meta_tagged": true,
        "status": "done",
        "video_url": "https://xxxx"
    },
    "message": "Success",
    "status": 10000,
    "request_id": "2025061718460554C9B78D23B0BAB45B2A",
    "time_elapsed": "508.312154ms"
}
```

---

## 720P图生视频-首帧

### 接口简介

根据输入的图片生成视频，以输入图片作为视频的第一帧。

### 提交任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_v30** |
| binary_data_base64 | array of string | 必选（二选一） | 图片文件base64编码，仅支持输入1张图片，仅支持JPEG、PNG格式 |
| image_urls | array of string | 必选（二选一） | 图片文件URL，仅支持输入1张图片 |
| prompt | string | 必选 | 用于生成视频的提示词 |
| seed | int | 可选 | 随机种子，默认-1 |
| frames | int | 可选 | 生成的总帧数，默认121（5秒） |

:::warning 图片限制
- 图片文件大小：最大 4.7MB
- 图片分辨率：最大 4096 * 4096，最短边不低于320
- 图片长边与短边比例在3以内
:::

#### 请求示例

```json
{
    "req_key": "jimeng_i2v_first_v30",
    "image_urls": [
        "https://xxx"
    ],
    "prompt": "千军万马",
    "seed": -1,
    "frames": 121
}
```

### 查询任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_v30** |
| task_id | string | 必选 | 任务ID |
| req_json | json string | 可选 | json序列化后的字符串，支持隐式水印配置 |

---

## 720P图生视频-首尾帧

### 接口简介

根据输入的首帧和尾帧图片生成视频，实现从首帧到尾帧的过渡动画。

### 提交任务

#### Body参数

| 参数 | 类型 | **可选/必首** | 说明 |
|------|------|-------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_tail_v30** |
| binary_data_base64 | array of string | 必选（二选一） | 图片文件base64编码，请输入2张图片 |
| image_urls | array of string | 必选（二选一） | 图片文件URL，请输入2张图片 |
| prompt | string | 必选 | 用于生成视频的提示词 |
| seed | int | 可选 | 随机种子，默认-1 |
| frames | int | 可选 | 生成的总帧数，默认121（5秒） |

:::warning 图片限制
- 图片文件大小：最大 4.7MB
- 图片分辨率：最大 4096 * 4096，最短边不低于320
- 图片长边与短边比例在3以内
- 尾帧图片需与首帧图片比例相同
:::

#### 请求示例

```json
{
    "req_key": "jimeng_i2v_first_tail_v30",
    "image_urls": [
        "https://xxx",
        "https://xxx"
    ],
    "prompt": "千军万马",
    "seed": -1,
    "frames": 121
}
```

### 查询任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_tail_v30** |
| task_id | string | 必选 | 任务ID |
| req_json | json string | 可选 | json序列化后的字符串，支持隐式水印配置 |

---

## 720P图生视频-运镜

### 接口简介

对输入的图片进行运镜处理，实现多种电影级运镜效果。

### 提交任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_recamera_v30** |
| binary_data_base64 | array of string | 必选（二选一） | 图片文件base64编码，仅支持输入1张图片 |
| image_urls | array of string | 必选（二选一） | 图片文件URL，仅支持输入1张图片 |
| prompt | string | 必选 | 用于生成视频的提示词 |
| template_id | string | 必选 | 运镜模板ID |
| camera_strength | string | 必选 | 强度 |
| seed | int | 可选 | 随机种子，默认-1 |
| frames | int | 可选 | 生成的总帧数，默认121（5秒） |

#### 运镜模板ID可选值

| 值 | 说明 |
|----|------|
| hitchcock_dolly_in | 希区柯克推进 |
| hitchcock_dolly_out | 希区柯克拉远 |
| robo_arm | 机械臂 |
| dynamic_orbit | 动感环绕 |
| central_orbit | 中心环绕 |
| crane_push | 起重机 |
| quick_pull_back | 超级拉远 |
| counterclockwise_swivel | 逆时针回旋 |
| clockwise_swivel | 顺时针回旋 |
| handheld | 手持运镜 |
| rapid_push_pull | 快速推拉 |

#### 强度可选值

| 值 | 说明 |
|----|------|
| weak | 弱 |
| medium | 中 |
| strong | 强 |

#### 请求示例

```json
{
    "req_key": "jimeng_i2v_recamera_v30",
    "image_urls": [
        "https://xxx"
    ],
    "prompt": "千军万马",
    "template_id": "hitchcock_dolly_in",
    "camera_strength": "medium",
    "seed": -1,
    "frames": 121
}
```

### 查询任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_recamera_v30** |
| task_id | string | 必选 | 任务ID |
| req_json | json string | 可选 | json序列化后的字符串，支持隐式水印配置 |

---

# 1080P视频生成

## 通用参数说明

以下参数适用于所有1080P视频生成接口：

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| prompt | string | 必选 | 用于生成视频的提示词，中英文均可输入。建议在400字以内，不超过800字，prompt过长有概率出现效果异常或不生效 |
| seed | int | 可选 | 随机种子，作为确定扩散初始状态的基础，默认-1（随机）。若随机种子为相同正整数且其他参数均一致，则生成视频极大概率效果一致。默认值：-1 |
| frames | int | 可选 | 生成的总帧数（帧数 = 24 * n + 1，其中n为秒数，支持5s、10s）。可选取值：[121, 241]，默认值：121 |

---

## 1080P文生视频

### 接口简介

即梦视频3.0文生视频能力，支持1080P超清渲染，准确遵循复杂指令，视觉表达流畅一致。

### 提交任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_t2v_v30_1080p** |
| prompt | string | 必选 | 用于生成视频的提示词 |
| seed | int | 可选 | 随机种子，默认-1 |
| frames | int | 可选 | 生成的总帧数，默认121（5秒） |
| aspect_ratio | string | 可选 | 生成视频的长宽比。可选取值：["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"]，默认值："16:9" |

#### 请求示例

```json
{
    "req_key": "jimeng_t2v_v30_1080p",
    "prompt": "千军万马",
    "seed": -1,
    "frames": 121,
    "aspect_ratio": "16:9"
}
```

#### 返回示例

```json
{
    "code": 10000,
    "data": {
        "task_id": "7392616336519610409"
    },
    "message": "Success",
    "request_id": "20240720103939AF0029465CF6A74E51EC",
    "time_elapsed": "104.852309ms"
}
```

### 查询任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_t2v_v30_1080p** |
| task_id | string | 必选 | 任务ID |
| req_json | json string | 可选 | json序列化后的字符串，支持隐式水印配置 |

---

## 1080P图生视频-首帧

### 接口简介

根据输入的图片生成1080P视频，以输入图片作为视频的第一帧。支持更高清的画面质量。

### 提交任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_v30_1080** |
| binary_data_base64 | array of string | 必选（二选一） | 图片文件base64编码，仅支持输入1张图片，仅支持JPEG、PNG格式 |
| image_urls | array of string | 必选（二选一） | 图片文件URL，仅支持输入1张图片 |
| prompt | string | 必选 | 用于生成视频的提示词 |
| seed | int | 可选 | 随机种子，默认-1 |
| frames | int | 可选 | 生成的总帧数，默认121（5秒） |

:::warning 图片限制
- 图片文件大小：最大 4.7MB
- 图片分辨率：最大 4096 * 4096，最短边不低于320
- 图片长边与短边比例在3以内
:::

#### 请求示例

```json
{
    "req_key": "jimeng_i2v_first_v30_1080",
    "image_urls": [
        "https://xxx"
    ],
    "prompt": "千军万马",
    "seed": -1,
    "frames": 121
}
```

### 查询任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_v30_1080** |
| task_id | string | 必选 | 任务ID |
| req_json | json string | 可选 | json序列化后的字符串，支持隐式水印配置 |

---

## 1080P图生视频-首尾帧

### 接口简介

根据输入的首帧和尾帧图片生成1080P视频，实现从首帧到尾帧的高清过渡动画。

### 提交任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_tail_v30_1080** |
| binary_data_base64 | array of string | 必选（二选一） | 图片文件base64编码，请输入2张图片 |
| image_urls | array of string | 必选（二选一） | 图片文件URL，请输入2张图片 |
| prompt | string | 必选 | 用于生成视频的提示词 |
| seed | int | 可选 | 随机种子，默认-1 |
| frames | int | 可选 | 生成的总帧数，默认121（5秒） |

:::warning 图片限制
- 图片文件大小：最大 4.7MB
- 图片分辨率：最大 4096 * 4096，最短边不低于320
- 图片长边与短边比例在3以内
- 尾帧图片需与首帧图片比例相同
:::

#### 请求示例

```json
{
    "req_key": "jimeng_i2v_first_tail_v30_1080",
    "image_urls": [
        "https://xxx",
        "https://xxx"
    ],
    "prompt": "千军万马",
    "seed": -1,
    "frames": 121
}
```

### 查询任务

#### Body参数

| 参数 | 类型 | **可选/必选** | 说明 |
|------|------|--------------|------|
| req_key | string | 必选 | 服务标识，取固定值：**jimeng_i2v_first_tail_v30_1080** |
| task_id | string | 必选 | 任务ID |
| req_json | json string | 可选 | json序列化后的字符串，支持隐式水印配置 |

---

# 服务标识汇总

| 功能 | 720P req_key | 1080P req_key |
|------|--------------|---------------|
| 文生视频 | jimeng_t2v_v30 | jimeng_t2v_v30_1080p |
| 图生视频-首帧 | jimeng_i2v_first_v30 | jimeng_i2v_first_v30_1080 |
| 图生视频-首尾帧 | jimeng_i2v_first_tail_v30 | jimeng_i2v_first_tail_v30_1080 |
| 图生视频-运镜 | jimeng_i2v_recamera_v30 | - |

---

# 接入说明

## SDK使用说明

请参考 [SDK使用说明](https://www.volcengine.com/docs/6444/1340578)

## HTTP方式接入说明

请参考 [HTTP请求示例](https://www.volcengine.com/docs/6444/1390583)

## Golang SDK

SDK地址：[https://github.com/volcengine/volc-sdk-golang](https://github.com/volcengine/volc-sdk-golang)

### 同步转异步提交任务示例

```Go
package main

import (
    "encoding/json"
    "fmt"
    "github.com/volcengine/volc-sdk-golang/service/visual"
)

func main() {
    testAk := "your ak"
    testSk := "your sk"

    visual.DefaultInstance.Client.SetAccessKey(testAk)
    visual.DefaultInstance.Client.SetSecretKey(testSk)

    reqBody := map[string]interface{}{
        "req_key": "jimeng_t2v_v30",
        "prompt": "千军万马",
        "seed": -1,
        "frames": 121,
        "aspect_ratio": "16:9"
    }

    resp, status, err := visual.DefaultInstance.CVSync2AsyncSubmitTask(reqBody)
    fmt.Println(status, err)
    b, _ := json.Marshal(resp)
    fmt.Println(string(b))
}
```

### 同步转异步查询任务示例

```Go
package main

import (
    "encoding/json"
    "fmt"
    "github.com/volcengine/volc-sdk-golang/service/visual"
)

func main() {
    testAk := "your ak"
    testSk := "your sk"

    visual.DefaultInstance.Client.SetAccessKey(testAk)
    visual.DefaultInstance.Client.SetSecretKey(testSk)

    reqBody := map[string]interface{}{
        "req_key": "jimeng_t2v_v30",
        "task_id": "7392616336519610409"
    }

    resp, status, err := visual.DefaultInstance.CVSync2AsyncGetResult(reqBody)
    fmt.Println(status, err)
    b, _ := json.Marshal(resp)
    fmt.Println(string(b))
}
```

## Python SDK

SDK地址：[https://github.com/volcengine/volc-sdk-python](https://github.com/volcengine/volc-sdk-python)

### 同步转异步提交任务示例

```Python
# coding:utf-8
from __future__ import print_function
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()
    visual_service.set_ak('your ak')
    visual_service.set_sk('your sk')

    form = {
        "req_key": "jimeng_t2v_v30",
        "prompt": "千军万马",
        "seed": -1,
        "frames": 121,
        "aspect_ratio": "16:9"
    }

    resp = visual_service.cv_sync2async_submit_task(form)
    print(resp)
```

### 同步转异步查询任务示例

```Python
# coding:utf-8
from __future__ import print_function
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()
    visual_service.set_ak('your ak')
    visual_service.set_sk('your sk')

    form = {
        "req_key": "jimeng_t2v_v30",
        "task_id": "7392616336519610409"
    }

    resp = visual_service.cv_sync2async_get_result(form)
    print(resp)
