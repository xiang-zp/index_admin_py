import requests
import json

print("=== 测试 OPTIONS 请求 ===")

# 测试代理 OPTIONS
print("\n1. 测试代理 OPTIONS (http://localhost:5175/api/admin/users/)")
try:
    resp = requests.options("http://localhost:5175/api/admin/users/")
    print(f"状态码: {resp.status_code}")
    print(f"响应头: {dict(resp.headers)}")
except Exception as e:
    print(f"错误: {e}")

# 测试后端直接 OPTIONS
print("\n2. 测试后端 OPTIONS (http://localhost:8000/api/admin/users/)")
try:
    resp = requests.options("http://localhost:8000/api/admin/users/")
    print(f"状态码: {resp.status_code}")
    print(f"响应头: {dict(resp.headers)}")
except Exception as e:
    print(f"错误: {e}")

# 测试 GET 请求（带认证）
print("\n3. 测试登录和GET请求")
login_resp = requests.post("http://localhost:8000/api/auth/admin/login", json={"username": "admin", "password": "admin123"})
if login_resp.status_code == 200:
    token = login_resp.json().get("data", {}).get("token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 通过代理GET
    print("\n通过代理GET:")
    get_resp = requests.get("http://localhost:5175/api/admin/users/", headers=headers)
    print(f"状态码: {get_resp.status_code}")
    print(f"响应头: {dict(get_resp.headers)}")
    
    # 直接后端GET
    print("\n直接后端GET:")
    get_resp2 = requests.get("http://localhost:8000/api/admin/users/", headers=headers)
    print(f"状态码: {get_resp2.status_code}")
    print(f"响应头: {dict(get_resp2.headers)}")