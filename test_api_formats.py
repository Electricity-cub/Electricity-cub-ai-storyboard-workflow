#!/usr/bin/env python3
"""
测试Coze API请求格式
"""

import requests
import json

API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNhMmE2OTQyLTU3N2EtNDUxYi1hOWYyLWE3MTk5M2I1OTU5YyJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIjZrZGF1aEFoN2VOUVczWUgwS3NYMjltcEs4SGJRRldiIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2MzMyNTkzLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI5MjQ5NTY5NTg2NDEzNTc4Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjI5MjkwMzk2MTI3ODU0NTkyIn0.SKYvYox0_8ojDtrNzk8DfwaecpQvLGl9eRCRCMFz3Imk-oScDXTyBKB_FNkAG3boS5tG2e75VQ-bVxB_LVakcDKXTU2zQ324PirHsoOL4qbdNz6hCokNgAUzNIedCNboN3DYZTyIGsDXL7K_wL18qJ1L7uxPVphOaq6mrAGOQ2E9F-4lhuBboVbv21iomfRiNV1xNviMPse9UhyreDTmBompWgdVBmD0LoLt6P1ghfrFCetyfhQa8NZEh6DxFv1ZuZ1yooaIVfJ51h_hI2WMBOHMSWdQh0g7WIkeR5XtyhNV_VFtEwAlAYOiJXVYZL21FeLvBHgcLUGuN0t2eF3H2A"

# 不同的请求格式测试
request_formats = [
    {
        "name": "格式1: 直接input",
        "url": "https://api.coze.cn/open_api/v1/chat",
        "data": {
            "input": {
                "script_content": "测试剧本",
                "episode_number": "ep01",
                "visual_style": "写实",
                "project_type": "国内短剧"
            }
        }
    },
    {
        "name": "格式2: 包含bot_id和query",
        "url": "https://api.coze.cn/open_api/v1/chat",
        "data": {
            "bot_id": "7629249569586413578",
            "user": "user123",
            "query": "帮我生成分镜，剧本：小明和小红在公园相遇",
            "stream": False
        }
    },
    {
        "name": "格式3: chat格式",
        "url": "https://api.coze.cn/open_api/v1/chat",
        "data": {
            "bot_id": "7629249569586413578",
            "user": "user123",
            "additional_messages": [
                {
                    "role": "user",
                    "content": "帮我生成分镜，剧本：小明和小红在公园相遇",
                    "content_type": "text"
                }
            ],
            "stream": False
        }
    },
    {
        "name": "格式4: workflow_run格式",
        "url": "https://api.coze.cn/open_api/v2/workflow/run",
        "data": {
            "workflow_id": "7629249569586413578",
            "parameters": {
                "script_content": "测试剧本",
                "episode_number": "ep01",
                "visual_style": "写实",
                "project_type": "国内短剧"
            }
        }
    }
]

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

print("=" * 80)
print("Coze API请求格式测试")
print("=" * 80)
print()

for i, test in enumerate(request_formats, 1):
    print(f"测试 {i}/{len(request_formats)}: {test['name']}")
    print("-" * 80)
    print(f"URL: {test['url']}")
    print(f"数据: {json.dumps(test['data'], indent=2, ensure_ascii=False)}")
    print()

    try:
        response = requests.post(
            test['url'],
            json=test['data'],
            headers=headers,
            timeout=10
        )

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功！")
            print("响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()
            print("=" * 80)
            print(f"🎉 找到正确的格式: {test['name']}")
            print("=" * 80)
            break
        else:
            print(f"❌ 状态码: {response.status_code}")
            print(f"响应: {response.text[:300]}")
            print()

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        print()

    print()
