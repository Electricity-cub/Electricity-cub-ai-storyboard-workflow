#!/usr/bin/env python3
"""
AI分镜师 - 后端代理服务
解决CORS跨域问题，安全地代理前端请求到Coze API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

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
    return jsonify({
        'status': 'healthy',
        'service': 'AI Storyboard Proxy'
    }), 200

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
            # 增加超时时间到600秒（10分钟），因为工作流包含多个LLM节点
            response = requests.post(
                COZE_API_URL,
                json=input_data,  # 直接传递input_data，不包装在input对象中
                headers=headers,
                timeout=(60, 600)  # (连接超时, 读取超时)
            )
        except requests.exceptions.Timeout:
            logger.error("Coze API请求超时（超过10分钟）")
            return jsonify({
                'error': '请求超时，工作流执行时间过长。请尝试简化剧本内容或稍后重试。'
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
