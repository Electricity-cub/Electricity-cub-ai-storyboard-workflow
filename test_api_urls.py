#!/usr/bin/env python3
"""
测试Coze API地址
"""

import requests
import json

# 你的Token
API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNhMmE2OTQyLTU3N2EtNDUxYi1hOWYyLWE3MTk5M2I1OTU5YyJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIjZrZGF1aEFoN2VOUVczWUgwS3NYMjltcEs4SGJRRldiIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2MzMyNTkzLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI5MjQ5NTY5NTg2NDEzNTc4Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjI5MjkwMzk2MTI3ODU0NTkyIn0.SKYvYox0_8ojDtrNzk8DfwaecpQvLGl9eRCRCMFz3Imk-oScDXTyBKB_FNkAG3boS5tG2e75VQ-bVxB_LVakcDKXTU2zQ324PirHsoOL4qbdNz6hCokNgAUzNIedCNboN3DYZTyIGsDXL7K_wL18qJ1L7uxPVphOaq6mrAGOQ2E9F-4lhuBboVbv21iomfRiNV1xNviMPse9UhyreDTmBompWgdVBmD0LoLt6P1ghfrFCetyfhQa8NZEh6DxFv1ZuZ1yooaIVfJ51h_hI2WMBOHMSWdQh0g7WIkeR5XtyhNV_VFtEwAlAYOiJXVYZL21FeLvBHgcLUGuN0t2eF3H2A"

# 要测试的API地址列表
API_URLS = [
    "https://api.coze.cn/open_api/v1/workflow/run",
    "https://api.coze.cn/open_api/v1/chat",
    "https://api.coze.cn/open_api/v2/bot/publish_workflow/run",
    "https://api.coze.cn/open_api/v2/workflow/run",
    "https://3b7j5mjhsz.coze.site/workflow_run",  # 你当前的配置
]

# 测试数据
test_data = {
    "input": {
        "script_content": "测试剧本",
        "episode_number": "ep01",
        "visual_style": "写实",
        "project_type": "国内短剧"
    }
}

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

print("=" * 60)
print("Coze API地址测试")
print("=" * 60)
print()

for i, url in enumerate(API_URLS, 1):
    print(f"测试 {i}/{len(API_URLS)}: {url}")
    print("-" * 60)

    try:
        response = requests.post(
            url,
            json=test_data,
            headers=headers,
            timeout=10
        )

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            print("✅ 成功！")
            print("响应:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            print()
            print("=" * 60)
            print(f"🎉 找到正确的API地址: {url}")
            print("=" * 60)
            break
        else:
            print(f"❌ 失败: {response.text[:200]}")
            print()

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        print()

    print()

print()
print("如果所有地址都测试失败，请检查：")
print("1. Token是否正确")
print("2. 工作流是否已发布")
print("3. 权限是否正确")
