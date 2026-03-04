import requests
import json

# 登录获取 token
login_url = "http://localhost:8000/api/auth/admin/login"
login_data = {"username": "admin", "password": "admin123"}

print("=== 测试登录 ===")
login_resp = requests.post(login_url, json=login_data)
print(f"登录状态: {login_resp.status_code}")

if login_resp.status_code == 200:
    login_json = login_resp.json()
    token = login_json.get("data", {}).get("token")
    print(f"Token 获取成功")
    
    # 测试获取用户列表 - 带斜杠
    headers = {"Authorization": f"Bearer {token}"}
    users_url_with_slash = "http://localhost:8000/api/admin/users/"
    users_url_no_slash = "http://localhost:8000/api/admin/users"
    
    print("\n=== 测试获取用户列表 (带斜杠) ===")
    users_resp = requests.get(users_url_with_slash, headers=headers)
    print(f"用户列表状态 (带斜杠): {users_resp.status_code}")
    print(f"用户列表响应: {users_resp.text[:500]}")
    
    print("\n=== 测试获取用户列表 (不带斜杠) ===")
    users_resp2 = requests.get(users_url_no_slash, headers=headers)
    print(f"用户列表状态 (不带斜杠): {users_resp2.status_code}")
    print(f"用户列表响应: {users_resp2.text[:500]}")
    
    # 测试 OPTIONS 请求
    print("\n=== 测试 OPTIONS 请求 ===")
    options_resp = requests.options(users_url_with_slash, headers=headers)
    print(f"OPTIONS 状态: {options_resp.status_code}")
    print(f"OPTIONS 响应头: {dict(options_resp.headers)}")
else:
    print("登录失败")