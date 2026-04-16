from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Coze API配置
COZE_API_URL = os.getenv("COZE_API_URL", "https://3b7j5mjhsz.coze.site/workflow_run")
API_TOKEN = os.getenv("API_TOKEN")

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    """生成分镜"""
    try:
        data = request.json

        # 验证必填字段
        if not data.get('script_content'):
            return jsonify({
                'success': False,
                'error': '剧本内容不能为空'
            }), 400

        # 构造请求参数
        coze_data = {
            "input": {
                "script_content": data.get('script_content', ''),
                "episode_number": data.get('episode_number', 'ep01'),
                "visual_style": data.get('visual_style', '写实'),
                "project_type": data.get('project_type', '国内短剧')
            }
        }

        # 调用Coze API
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(COZE_API_URL, headers=headers, json=coze_data)
        response.raise_for_status()

        result = response.json()

        return jsonify({
            'success': True,
            'data': result
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'API调用失败: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Storyboard Web App'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
