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
COZE_API_URL = "https://3b7j5mjhsz.coze.site/workflow_run"
COZE_API_TOKEN = "你的Coze_API_Token"  # 替换成你的实际Token

@app.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Storyboard Proxy'
    }), 200

@app.route('/api/v1/generate', methods=['POST'])
def generate_storyboard():
    """
    代理前端请求到Coze工作流API
    """
    try:
        # 获取前端请求的数据
        data = request.json

        # 验证必填字段
        if not data or 'input' not in data:
            logger.error("请求缺少input字段")
            return jsonify({
                'error': '缺少input字段'
            }), 400

        input_data = data['input']

        # 验证剧本内容
        if not input_data.get('script_content'):
            logger.error("剧本内容为空")
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

        # 构造Coze API请求
        headers = {
            'Authorization': f'Bearer {COZE_API_TOKEN}',
            'Content-Type': 'application/json'
        }

        # 调用Coze API
        response = requests.post(
            COZE_API_URL,
            json={'input': input_data},
            headers=headers,
            timeout=300  # 5分钟超时
        )

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
