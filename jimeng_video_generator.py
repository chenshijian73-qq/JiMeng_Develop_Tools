#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦AI视频批量生成工具
用于批量根据图片生成视频，支持多产品目录并发处理

使用方法:
    python jimeng_video_generator.py

环境变量:
    JIMENG_AK: 访问密钥AK
    JIMENG_SK: 访问密钥SK
"""

import os
import sys
import json
import time
import glob
import asyncio
import aiohttp
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor

import tomli


# ==================== 配置类 ====================

@dataclass
class GlobalConfig:
    """全局配置"""
    prompt: str = "自然流畅的过渡动画"
    frames: int = 121
    image_dir: str = "products"
    req_key_720p: str = "jimeng_i2v_first_v30"
    req_key_1080p: str = "jimeng_i2v_first_v30_1080"
    quality: str = "720p"


@dataclass
class ProductConfig:
    """产品配置"""
    prompt: Optional[str] = None
    frames: Optional[int] = None
    description: str = ""  # 产品描述信息
    image_dir: Optional[str] = None  # 独立图片目录


@dataclass
class VideoTask:
    """视频生成任务"""
    product_name: str
    image_path: str
    output_path: str
    prompt: str
    frames: int
    quality: str
    req_key: str


@dataclass
class VideoResult:
    """视频生成结果"""
    task: VideoTask
    success: bool
    task_id: Optional[str] = None
    video_url: Optional[str] = None
    error: Optional[str] = None


# ==================== API客户端 ====================

class JimengVideoClient:
    """即梦AI视频生成API客户端"""
    
    BASE_URL = "https://visual.volcengineapi.com"
    SUBMIT_ACTION = "CVSync2AsyncSubmitTask"
    QUERY_ACTION = "CVSync2AsyncGetResult"
    VERSION = "2022-08-31"
    
    def __init__(self, ak: str, sk: str, quality: str = "720p"):
        self.ak = ak
        self.sk = sk
        self.quality = quality
        self.region = "cn-north-1"
        self.service = "cv"
    
    def _generate_signature(self, method: str, action: str, body: str = "") -> Dict[str, str]:
        """生成火山引擎API签名（简化版）"""
        import hashlib
        import hmac
        import base64
        from datetime import datetime
        
        # 这里使用简化的签名方式，实际生产环境请参考火山引擎官方签名算法
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date = timestamp[:8]
        
        # 简化签名（实际需要完整的签名算法）
        headers = {
            "Content-Type": "application/json",
            "X-Date": timestamp,
            "X-Region": self.region,
            "X-Service": self.service,
        }
        
        return headers
    
    async def submit_task(
        self, 
        session: aiohttp.ClientSession,
        image_url: str, 
        prompt: str, 
        frames: int = 121,
        req_key: str = "jimeng_i2v_first_v30"
    ) -> Dict[str, Any]:
        """提交视频生成任务"""
        url = f"{self.BASE_URL}?Action={self.SUBMIT_ACTION}&Version={self.VERSION}"
        
        payload = {
            "req_key": req_key,
            "image_urls": [image_url],
            "prompt": prompt,
            "frames": frames
        }
        
        headers = self._generate_signature("POST", self.SUBMIT_ACTION)
        headers["Content-Type"] = "application/json"
        
        # 添加鉴权信息
        headers["X-AK"] = self.ak
        headers["X-SK"] = self.sk
        
        async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            return await resp.json()
    
    async def query_task(
        self, 
        session: aiohttp.ClientSession,
        task_id: str,
        req_key: str = "jimeng_i2v_first_v30"
    ) -> Dict[str, Any]:
        """查询任务状态"""
        url = f"{self.BASE_URL}?Action={self.QUERY_ACTION}&Version={self.VERSION}"
        
        payload = {
            "req_key": req_key,
            "task_id": task_id
        }
        
        headers = self._generate_signature("POST", self.QUERY_ACTION)
        headers["Content-Type"] = "application/json"
        headers["X-AK"] = self.ak
        headers["X-SK"] = self.sk
        
        async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            return await resp.json()


class JimengVideoClientSync:
    """同步版本的即梦AI视频生成API客户端（使用requests）"""
    
    BASE_URL = "https://visual.volcengineapi.com"
    SUBMIT_ACTION = "CVSync2AsyncSubmitTask"
    QUERY_ACTION = "CVSync2AsyncGetResult"
    VERSION = "2022-08-31"
    
    def __init__(self, ak: str, sk: str, quality: str = "720p"):
        self.ak = ak
        self.sk = sk
        self.quality = quality
        self.region = "cn-north-1"
        self.service = "cv"
    
    def submit_task(
        self, 
        image_url: str, 
        prompt: str, 
        frames: int = 121,
        req_key: str = "jimeng_i2v_first_v30"
    ) -> Dict[str, Any]:
        """提交视频生成任务"""
        import requests
        
        url = f"{self.BASE_URL}?Action={self.SUBMIT_ACTION}&Version={self.VERSION}"
        
        payload = {
            "req_key": req_key,
            "image_urls": [image_url],
            "prompt": prompt,
            "frames": frames
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-AK": self.ak,
            "X-SK": self.sk
        }
        
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            return resp.json()
        except Exception as e:
            return {"code": -1, "message": str(e)}
    
    def query_task(
        self, 
        task_id: str,
        req_key: str = "jimeng_i2v_first_v30"
    ) -> Dict[str, Any]:
        """查询任务状态"""
        import requests
        
        url = f"{self.BASE_URL}?Action={self.QUERY_ACTION}&Version={self.VERSION}"
        
        payload = {
            "req_key": req_key,
            "task_id": task_id
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-AK": self.ak,
            "X-SK": self.sk
        }
        
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            return resp.json()
        except Exception as e:
            return {"code": -1, "message": str(e)}


# ==================== 配置加载 ====================

def load_global_config(config_path: str = "config.toml") -> GlobalConfig:
    """加载全局配置文件"""
    if not os.path.exists(config_path):
        print(f"警告: 全局配置文件 {config_path} 不存在，使用默认配置")
        return GlobalConfig()
    
    with open(config_path, "rb") as f:
        config = tomli.load(f)
    
    default_cfg = config.get("default", {})
    output_cfg = config.get("output", {})
    api_cfg = config.get("api", {})
    
    return GlobalConfig(
        prompt=default_cfg.get("prompt", "自然流畅的过渡动画"),
        frames=default_cfg.get("frames", 121),
        image_dir=output_cfg.get("image_dir", "products"),
        req_key_720p=api_cfg.get("req_key_720p", "jimeng_i2v_first_v30"),
        req_key_1080p=api_cfg.get("req_key_1080p", "jimeng_i2v_first_v30_1080"),
        quality=api_cfg.get("quality", "720p")
    )


def load_product_config(product_dir: str, global_config: GlobalConfig) -> ProductConfig:
    """加载产品目录的配置文件"""
    product_config_path = os.path.join(product_dir, "config.toml")
    
    if not os.path.exists(product_config_path):
        # 如果没有独立配置，使用全局配置
        return ProductConfig()
    
    with open(product_config_path, "rb") as f:
        config = tomli.load(f)
    
    default_cfg = config.get("default", {})
    
    return ProductConfig(
        prompt=default_cfg.get("prompt"),
        frames=default_cfg.get("frames"),
        description=config.get("product", {}).get("description", ""),
        image_dir=config.get("product", {}).get("image_dir")
    )


def merge_config(
    global_config: GlobalConfig, 
    product_config: ProductConfig
) -> Dict[str, Any]:
    """合并全局配置和产品配置"""
    return {
        "prompt": product_config.prompt or global_config.prompt,
        "frames": product_config.frames or global_config.frames,
        "description": product_config.description,
        "quality": global_config.quality,
        "req_key": global_config.req_key_1080p if global_config.quality == "1080p" else global_config.req_key_720p
    }


# ==================== 目录扫描 ====================

def get_product_directories(base_dir: str) -> List[str]:
    """获取所有产品目录"""
    if not os.path.exists(base_dir):
        print(f"错误: 产品目录 {base_dir} 不存在")
        return []
    
    dirs = [d for d in os.listdir(base_dir) 
            if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith('.')]
    
    return sorted(dirs)


def get_images_in_directory(dir_path: str) -> List[str]:
    """获取目录中的所有图片文件"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    images = []
    
    for ext in image_extensions:
        images.extend(glob.glob(os.path.join(dir_path, f"*{ext}")))
        images.extend(glob.glob(os.path.join(dir_path, f"*{ext.upper()}")))
    
    return sorted(images)


# ==================== 视频生成 ====================

def create_image_url(image_path: str, base_url: str = "") -> str:
    """创建图片URL（这里需要根据实际部署情况配置）"""
    # 如果有HTTP服务，可以返回实际的URL
    # 这里暂时返回本地路径，生产环境需要配置图片服务器
    if base_url:
        filename = os.path.basename(image_path)
        return f"{base_url}/{filename}"
    
    # 简化处理：假设使用本地文件路径
    return f"file://{os.path.abspath(image_path)}"


async def process_single_task(
    client: JimengVideoClient,
    task: VideoTask,
    semaphore: asyncio.Semaphore
) -> VideoResult:
    """处理单个视频生成任务"""
    async with semaphore:
        print(f"[{task.product_name}] 提交任务: {os.path.basename(task.image_path)}")
        
        try:
            # 提交任务
            async with aiohttp.ClientSession() as session:
                submit_result = await client.submit_task(
                    session=session,
                    image_url=task.image_path,
                    prompt=task.prompt,
                    frames=task.frames,
                    req_key=task.req_key
                )
            
            if submit_result.get("code") != 10000:
                return VideoResult(
                    task=task,
                    success=False,
                    error=submit_result.get("message", "提交失败")
                )
            
            task_id = submit_result.get("data", {}).get("task_id")
            print(f"[{task.product_name}] 任务已提交, task_id: {task_id}")
            
            # 轮询查询任务状态
            max_retries = 60  # 最多等待60次
            retry_interval = 3  # 每3秒查询一次
            
            for i in range(max_retries):
                await asyncio.sleep(retry_interval)
                
                async with aiohttp.ClientSession() as session:
                    query_result = await client.query_task(
                        session=session,
                        task_id=task_id,
                        req_key=task.req_key
                    )
                
                if query_result.get("code") != 10000:
                    continue
                
                status = query_result.get("data", {}).get("status")
                
                if status == "done":
                    video_url = query_result.get("data", {}).get("video_url")
                    print(f"[{task.product_name}] 视频生成完成: {video_url}")
                    return VideoResult(
                        task=task,
                        success=True,
                        task_id=task_id,
                        video_url=video_url
                    )
                elif status in ["not_found", "expired"]:
                    return VideoResult(
                        task=task,
                        success=False,
                        task_id=task_id,
                        error=f"任务状态: {status}"
                    )
                else:
                    print(f"[{task.product_name}] 任务处理中... ({i+1}/{max_retries})")
            
            return VideoResult(
                task=task,
                success=False,
                task_id=task_id,
                error="等待超时"
            )
            
        except Exception as e:
            return VideoResult(
                task=task,
                success=False,
                error=str(e)
            )


def process_single_task_sync(
    client: JimengVideoClientSync,
    task: VideoTask,
    max_wait_time: int = 180
) -> VideoResult:
    """同步版本：处理单个视频生成任务"""
    print(f"[{task.product_name}] 提交任务: {os.path.basename(task.image_path)}")
    
    try:
        # 提交任务
        submit_result = client.submit_task(
            image_url=task.image_path,
            prompt=task.prompt,
            frames=task.frames,
            req_key=task.req_key
        )
        
        if submit_result.get("code") != 10000:
            return VideoResult(
                task=task,
                success=False,
                error=submit_result.get("message", "提交失败")
            )
        
        task_id = submit_result.get("data", {}).get("task_id")
        print(f"[{task.product_name}] 任务已提交, task_id: {task_id}")
        
        # 轮询查询任务状态
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            time.sleep(3)
            
            query_result = client.query_task(
                task_id=task_id,
                req_key=task.req_key
            )
            
            if query_result.get("code") != 10000:
                continue
            
            status = query_result.get("data", {}).get("status")
            
            if status == "done":
                video_url = query_result.get("data", {}).get("video_url")
                print(f"[{task.product_name}] 视频生成完成: {video_url}")
                return VideoResult(
                    task=task,
                    success=True,
                    task_id=task_id,
                    video_url=video_url
                )
            elif status in ["not_found", "expired"]:
                return VideoResult(
                    task=task,
                    success=False,
                    task_id=task_id,
                    error=f"任务状态: {status}"
                )
            else:
                elapsed = int(time.time() - start_time)
                print(f"[{task.product_name}] 任务处理中... ({elapsed}s)")
        
        return VideoResult(
            task=task,
            success=False,
            task_id=task_id,
            error="等待超时"
        )
        
    except Exception as e:
        return VideoResult(
            task=task,
            success=False,
            error=str(e)
        )


# ==================== 主程序 ====================

def generate_video_tasks(
    global_config: GlobalConfig,
    products_dir: str
) -> List[VideoTask]:
    """生成所有视频任务"""
    tasks = []
    products = get_product_directories(products_dir)
    
    print(f"发现 {len(products)} 个产品目录")
    
    for product_name in products:
        product_dir = os.path.join(products_dir, product_name)
        product_config = load_product_config(product_dir, global_config)
        config = merge_config(global_config, product_config)
        
        # 确定图片目录
        image_dir = product_config.image_dir if product_config.image_dir else product_dir
        
        # 获取图片列表
        images = get_images_in_directory(image_dir)
        
        if not images:
            print(f"[{product_name}] 警告: 目录中没有图片")
            continue
        
        print(f"[{product_name}] 找到 {len(images)} 张图片")
        
        # 为每张图片创建任务
        for idx, image_path in enumerate(images):
            # 创建输出目录
            output_dir = os.path.join(product_dir, "videos")
            os.makedirs(output_dir, exist_ok=True)
            
            # 输出文件名
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}_video.mp4")
            
            task = VideoTask(
                product_name=product_name,
                image_path=image_path,
                output_path=output_path,
                prompt=config["prompt"],
                frames=config["frames"],
                quality=config["quality"],
                req_key=config["req_key"]
            )
            tasks.append(task)
    
    return tasks


async def run_async(concurrency: int = 2):
    """异步运行主程序"""
    # 加载配置
    global_config = load_global_config()
    
    # 获取AK/SK
    ak = os.environ.get("JIMENG_AK")
    sk = os.environ.get("JIMENG_SK")
    
    if not ak or not sk:
        print("错误: 请设置环境变量 JIMENG_AK 和 JIMENG_SK")
        print("例如: export JIMENG_AK=your_ak JIMENG_SK=your_sk")
        sys.exit(1)
    
    # 创建客户端
    client = JimengVideoClient(ak, sk, global_config.quality)
    
    # 生成任务
    products_dir = global_config.image_dir
    tasks = generate_video_tasks(global_config, products_dir)
    
    if not tasks:
        print("没有找到任何视频生成任务")
        return
    
    print(f"共 {len(tasks)} 个任务，并发数: {concurrency}")
    
    # 创建信号量控制并发
    semaphore = asyncio.Semaphore(concurrency)
    
    # 执行任务
    results = await asyncio.gather(
        *[process_single_task(client, task, semaphore) for task in tasks]
    )
    
    # 输出结果统计
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count
    
    print("\n" + "=" * 50)
    print(f"任务完成统计:")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print("=" * 50)
    
    # 保存结果到文件
    results_file = "video_generation_results.json"
    results_data = []
    for r in results:
        results_data.append({
            "product": r.task.product_name,
            "image": os.path.basename(r.task.image_path),
            "success": r.success,
            "task_id": r.task_id,
            "video_url": r.video_url,
            "error": r.error
        })
    
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {results_file}")


def run_sync(concurrency: int = 2):
    """同步运行主程序"""
    # 加载配置
    global_config = load_global_config()
    
    # 获取AK/SK
    ak = os.environ.get("JIMENG_AK")
    sk = os.environ.get("JIMENG_SK")
    
    if not ak or not sk:
        print("错误: 请设置环境变量 JIMENG_AK 和 JIMENG_SK")
        print("例如: export JIMENG_AK=your_ak JIMENG_SK=your_sk")
        sys.exit(1)
    
    # 创建客户端
    client = JimengVideoClientSync(ak, sk, global_config.quality)
    
    # 生成任务
    products_dir = global_config.image_dir
    tasks = generate_video_tasks(global_config, products_dir)
    
    if not tasks:
        print("没有找到任何视频生成任务")
        return
    
    print(f"共 {len(tasks)} 个任务，并发数: {concurrency}")
    
    # 使用线程池控制并发（同步版本）
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(
            lambda task: process_single_task_sync(client, task),
            tasks
        ))
    
    # 输出结果统计
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count
    
    print("\n" + "=" * 50)
    print(f"任务完成统计:")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print("=" * 50)
    
    # 保存结果到文件
    results_file = "video_generation_results.json"
    results_data = []
    for r in results:
        results_data.append({
            "product": r.task.product_name,
            "image": os.path.basename(r.task.image_path),
            "success": r.success,
            "task_id": r.task_id,
            "video_url": r.video_url,
            "error": r.error
        })
    
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {results_file}")


def main():
    parser = argparse.ArgumentParser(description="即梦AI视频批量生成工具")
    parser.add_argument("-c", "--concurrency", type=int, default=2, 
                        help="并发数，默认2")
    parser.add_argument("-s", "--sync", action="store_true",
                        help="使用同步模式（默认异步）")
    parser.add_argument("--config", default="config.toml",
                        help="配置文件路径")
    
    args = parser.parse_args()
    
    print("即梦AI视频批量生成工具")
    print("=" * 50)
    
    if args.sync:
        run_sync(args.concurrency)
    else:
        asyncio.run(run_async(args.concurrency))


if __name__ == "__main__":
    main()
