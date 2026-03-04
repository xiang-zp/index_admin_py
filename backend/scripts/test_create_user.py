import requests
import json

# 先登录获取token
print("=== 登录获取token ===")
login_url = "http://localhost:8000/api/auth/admin/login"
login_data = {"username": "admin", "password": "admin123"}

login_resp = requests.post(login_url, json=login_data)
print(f"登录状态: {login_resp.status_code}")
if login_resp.status_code != 200:
    print(f"登录失败: {login_resp.text}")
    exit(1)

login_json = login_resp.json()
token = login_json.get("data", {}).get("token")
print(f"Token获取成功")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 测试创建用户
print("\n=== 测试创建用户 ===")
create_url = "http://localhost:8000/api/admin/users/"
create_data = {
    "username": "testuser_" + str(hash("test") % 10000),
    "password": "test123",
    "role": "editor"
}

print(f"创建用户数据: {create_data}")

try:
    create_resp = requests.post(create_url, json=create_data, headers=headers)
    print(f"创建用户状态码: {create_resp.status_code}")
    print(f"创建用户响应头: {dict(create_resp.headers)}")
    print(f"创建用户响应体: {create_resp.text}")
    
    if create_resp.status_code != 200:
        print("\n尝试分析错误:")
        try:
            error_json = create_resp.json()
            print(f"错误JSON: {json.dumps(error_json, indent=2, ensure_ascii=False)}")
        except:
            print(f"响应不是JSON: {create_resp.text[:200]}")
except Exception as e:
    print(f"请求异常: {e}")
    import traceback
    traceback.print_exc()

# 测试获取用户列表
print("\n=== 测试获取用户列表 ===")
get_resp = requests.get(create_url, headers=headers)
print(f"获取用户列表状态码: {get_resp.status_code}")
if get_resp.status_code == 200:
    users_json = get_resp.json()
    print(f"当前用户数量: {len(users_json.get('data', []))}")
    print(f"第一个用户: {json.dumps(users_json.get('data', [])[0] if users_json.get('data') else {}, indent=2, ensure_ascii=False)[:200]}...")
else:
    print(f"获取用户列表失败: {get_resp.text[:200]}")