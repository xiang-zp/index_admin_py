# -*- coding: utf-8 -*-
import requests
import json

# 先登录获取token
login_data = {
    "username": "admin",
    "password": "admin123"
}

try:
    # 登录
    login_resp = requests.post(
        "http://localhost:8000/api/auth/admin/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    print("=== 登录响应 ===")
    print(f"Status: {login_resp.status_code}")
    print(f"Response: {login_resp.text[:500]}")

    if login_resp.status_code == 200:
        login_json = login_resp.json()
        token = login_json.get("data", {}).get("token")
        print(f"\nToken获取成功: {token[:50]}...")

        # 用token请求用户列表
        users_resp = requests.get(
            "http://localhost:8000/api/admin/users",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        print("\n=== 用户列表响应 ===")
        print(f"Status: {users_resp.status_code}")
        print(f"Response: {users_resp.text[:1000]}")

        if users_resp.status_code == 200:
            users_json = users_resp.json()
            print(f"\n=== 解析数据 ===")
            print(f"Code: {users_json.get('code')}")
            print(f"Message: {users_json.get('message')}")
            data = users_json.get('data', [])
            print(f"用户数量: {len(data)}")
            if data:
                print(f"第一个用户: {json.dumps(data[0], ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"Error: {e}")
