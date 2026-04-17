#!/usr/bin/env python3
"""
AI分镜师 - 后端代理服务
解决CORS跨域问题，安全地代理前端请求到Coze API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
from task_manager import create_task, get_task_status, cleanup_old_tasks

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

# Coze API配置
COZE_API_URL = "https://3b7j5mjhsz.coze.site/run"
COZE_API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNhMmE2OTQyLTU3N2EtNDUxYi1hOWYyLWE3MTk5M2I1OTU5YyJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIjZrZGF1aEFoN2VOUVczWUgwS3NYMjltcEs4SGJRRldiIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2MzMyNTkzLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI5MjQ5NTY5NTg2NDEzNTc4Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjI5MjkwMzk2MTI3ODU0NTkyIn0.SKYvYox0_8ojDtrNzk8DfwaecpQvLGl9eRCRCMFz3Imk-oScDXTyBKB_FNkAG3boS5tG2e75VQ-bVxB_LVakcDKXTU2zQ324PirHsoOL4qbdNz6hCokNgAUzNIedCNboN3DYZTyIGsDXL7K_wL18qJ1L7uxPVphOaq6mrAGOQ2E9F-4lhuBboVbv21iomfRiNV1xNviMPse9UhyreDTmBompWgdVBmD0LoLt6P1ghfrFCetyfhQa8NZEh6DxFv1ZuZ1yooaIVfJ51h_hI2WMBOHMSWdQh0g7WIkeR5XtyhNV_VFtEwAlAYOiJXVYZL21FeLvBHgcLUGuN0t2eF3H2A"  # 替换成你的实际Token

@app.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    # 定期清理旧任务
    cleanup_count = cleanup_old_tasks()
    if cleanup_count > 0:
        logger.info(f"清理了 {cleanup_count} 个旧任务")

    return jsonify({
        'status': 'healthy',
        'service': 'AI Storyboard Proxy',
        'active_tasks': len([t for t in globals().get('tasks', {}).values() if t.status == 'running'])
    }), 200

# ==================== 异步API接口 ====================

@app.route('/api/v1/tasks', methods=['POST'])
def create_async_task():
    """
    创建异步任务（推荐用于长时间工作流）
    返回任务ID，可以轮询任务状态
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求体不能为空'}), 400

        # 支持两种格式
        if 'input' in data:
            input_data = data['input']
        else:
            input_data = data

        # 验证剧本内容
        if not input_data.get('script_content'):
            return jsonify({'error': '剧本内容不能为空'}), 400

        # 验证Token
        if COZE_API_TOKEN == "你的Coze_API_Token" or not COZE_API_TOKEN:
            return jsonify({'error': 'API Token未配置'}), 500

        logger.info(f"创建异步任务: episode={input_data.get('episode_number')}, style={input_data.get('visual_style')}")

        # 创建异步任务
        task_id = create_task(COZE_API_URL, COZE_API_TOKEN, input_data)

        return jsonify({
            'task_id': task_id,
            'status': 'pending',
            'message': '任务已创建，正在后台执行。使用 task_id 查询任务状态。',
            'query_url': f'/api/v1/tasks/{task_id}'
        }), 201

    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        return jsonify({'error': f'创建任务失败: {str(e)}'}), 500


@app.route('/api/v1/tasks/<task_id>', methods=['GET'])
def get_task(task_id: str):
    """
    查询任务状态
    """
    try:
        task = get_task_status(task_id)

        if task is None:
            return jsonify({'error': '任务不存在'}), 404

        return jsonify(task), 200

    except Exception as e:
        logger.error(f"查询任务失败: {str(e)}")
        return jsonify({'error': f'查询任务失败: {str(e)}'}), 500

# ==================== 同步API接口（原有） ====================

@app.route('/run', methods=['POST'])
def run():
    """生成接口（别名，兼容旧版）"""
    return generate_storyboard()

@app.route('/api/v1/generate', methods=['POST'])
def generate_storyboard():
    """
    代理前端请求到Coze工作流API
    """
    try:
        # 获取前端请求的数据
        data = request.json

        # 验证必填字段
        if not data:
            logger.error("请求体为空")
            return jsonify({
                'error': '请求体不能为空'
            }), 400

        # 支持两种格式：
        # 格式1: {"input": {...}}
        # 格式2: 直接 {...}
        if 'input' in data:
            input_data = data['input']
        else:
            input_data = data

        # 验证剧本内容
        if not input_data.get('script_content'):
            logger.error(f"剧本内容为空, input_data={input_data}")
            return jsonify({
                'error': '剧本内容不能为空'
            }), 400

        # 验证Token
        if COZE_API_TOKEN == "你的Coze_API_Token" or not COZE_API_TOKEN:
            logger.error("API Token未配置")
            return jsonify({
                'error': 'API Token未配置，请在app.py中设置COZE_API_TOKEN'
            }), 500

        logger.info(f"收到请求: episode={input_data.get('episode_number')}, style={input_data.get('visual_style')}")
        logger.info("开始调用Coze API，这可能需要较长时间（多个LLM节点串行执行）...")

        # 构造Coze API请求
        headers = {
            'Authorization': f'Bearer {COZE_API_TOKEN}',
            'Content-Type': 'application/json'
        }

        try:
            # 调用Coze API
            # 增加超时时间到1200秒（20分钟），因为工作流包含多个LLM节点
            # 每个LLM节点可能需要1-3分钟，5个节点串行执行可能需要5-15分钟
            logger.info("超时设置: 连接60秒, 读取1200秒（20分钟）")
            response = requests.post(
                COZE_API_URL,
                json=input_data,  # 直接传递input_data，不包装在input对象中
                headers=headers,
                timeout=(60, 1200)  # (连接超时, 读取超时)
            )
            logger.info(f"Coze API响应状态: {response.status_code}")
        except requests.exceptions.Timeout:
            logger.error("Coze API请求超时（超过20分钟）")
            return jsonify({
                'error': '请求超时，工作流执行时间超过20分钟。这可能是因为：\n1. 剧本内容过长\n2. 网络连接不稳定\n3. Coze服务繁忙\n\n建议：\n- 尝试简化剧本内容（<300字，<5个场景）\n- 稍后重试\n- 检查网络连接'
            }), 504
        except requests.exceptions.RequestException as e:
            logger.error(f"Coze API请求异常: {str(e)}")
            return jsonify({
                'error': f'请求失败: {str(e)}'
            }), 500

        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            logger.info("Coze API调用成功")
            return jsonify(result), 200
        else:
            logger.error(f"Coze API返回错误: {response.status_code}")
            return jsonify({
                'error': f'Coze API错误: {response.status_code}',
                'details': response.text
            }), response.status_code

    except requests.exceptions.Timeout:
        logger.error("请求超时")
        return jsonify({
            'error': '请求超时，请稍后重试'
        }), 504

    except requests.exceptions.RequestException as e:
        logger.error(f"请求异常: {str(e)}")
        return jsonify({
            'error': f'网络请求失败: {str(e)}'
        }), 500

    except Exception as e:
        logger.error(f"服务器错误: {str(e)}")
        return jsonify({
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    logger.info("AI分镜师后端服务启动中...")
    logger.info(f"Coze API URL: {COZE_API_URL}")
    logger.info(f"Token已配置: {'是' if COZE_API_TOKEN != '你的Coze_API_Token' else '否'}")

    # 启动服务
    app.run(
        host='0.0.0.0',  # 允许外部访问
        port=5000,
        debug=True
    )
