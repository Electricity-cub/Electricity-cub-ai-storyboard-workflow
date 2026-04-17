#!/usr/bin/env python3
"""
测试Coze API请求格式（完整版）
"""

import requests
import json

API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNhMmE2OTQyLTU3N2EtNDUxYi1hOWYyLWE3MTk5M2I1OTU5YyJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIjZrZGF1aEFoN2VOUVczWUgwS3NYMjltcEs4SGJRRldiIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2MzMyNTkzLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI5MjQ5NTY5NTg2NDEzNTc4Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjI5MjkwMzk2MTI3ODU0NTkyIn0.SKYvYox0_8ojDtrNzk8DfwaecpQvLGl9eRCRCMFz3Imk-oScDXTyBKB_FNkAG3boS5tG2e75VQ-bVxB_LVakcDKXTU2zQ324PirHsoOL4qbdNz6hCokNgAUzNIedCNboN3DYZTyIGsDXL7K_wL18qJ1L7uxPVphOaq6mrAGOQ2E9F-4lhuBboVbv21iomfRiNV1xNviMPse9UhyreDTmBompWgdVBmD0LoLt6P1ghfrFCetyfhQa8NZEh6DxFv1ZuZ1yooaIVfJ51h_hI2WMBOHMSWdQh0g7WIkeR5XtyhNV_VFtEwAlAYOiJXVYZL21FeLvBHgcLUGuN0t2eF3H2A"

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

print("=" * 80)
print("测试2: 包含bot_id和query")
print("=" * 80)

test_data = {
    "bot_id": "7629249569586413578",
    "user": "user123",
    "query": "帮我生成分镜，剧本：小明和小红在公园相遇",
    "stream": False
}

try:
    response = requests.post(
        "https://api.coze.cn/open_api/v1/chat",
        json=test_data,
        headers=headers,
        timeout=30
    )

    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    if response.status_code == 200 and response.json().get('code') == 0:
        print("\n✅ 成功！这个格式可用")

except Exception as e:
    print(f"❌ 错误: {str(e)}")
