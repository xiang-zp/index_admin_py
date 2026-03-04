import requests
import json
import sys

print("=== 创建用户调试 ===")

# 设置详细的请求日志
import http.client as http_client
import logging
http_client.HTTPConnection.debuglevel = 1

# 配置日志
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# 先登录获取token
print("\n1. 登录")
login_url = "http://localhost:8000/api/auth/admin/login"
login_data = {"username": "admin", "password": "admin123"}

try:
    login_resp = requests.post(login_url, json=login_data)
    print(f"登录状态码: {login_resp.status_code}")
    print(f"登录响应: {login_resp.text[:200]}")
    
    if login_resp.status_code != 200:
        print("登录失败")
        sys.exit(1)
        
    login_json = login_resp.json()
    token = login_json.get("data", {}).get("token")
    print(f"Token: {token[:50]}...")
    
except Exception as e:
    print(f"登录异常: {e}")
    sys.exit(1)

# 测试创建用户
print("\n2. 创建用户")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

create_url = "http://localhost:8000/api/admin/users/"
create_data = {
    "username": "testuser_" + str(abs(hash("test")) % 10000),
    "password": "test123",
    "role": "editor"
}

print(f"请求URL: {create_url}")
print(f"请求头: {json.dumps(headers, indent=2)}")
print(f"请求体: {json.dumps(create_data, indent=2)}")

try:
    create_resp = requests.post(create_url, json=create_data, headers=headers)
    print(f"\n响应状态码: {create_resp.status_code}")
    print(f"响应头: {json.dumps(dict(create_resp.headers), indent=2)}")
    print(f"响应体: {create_resp.text}")
    
    # 尝试解析响应
    if create_resp.text:
        try:
            resp_json = create_resp.json()
            print(f"\n解析后的JSON: {json.dumps(resp_json, indent=2, ensure_ascii=False)}")
            
            if resp_json.get("code") != 200 and resp_json.get("code") != 0:
                print(f"错误代码: {resp_json.get('code')}")
                print(f"错误信息: {resp_json.get('message')}")
        except json.JSONDecodeError:
            print("响应不是有效的JSON")
    
except Exception as e:
    print(f"\n请求异常: {e}")
    import traceback
    traceback.print_exc()

# 测试GET请求
print("\n3. 获取用户列表")
try:
    get_resp = requests.get(create_url, headers=headers)
    print(f"GET状态码: {get_resp.status_code}")
    
    if get_resp.status_code == 200:
        get_json = get_resp.json()
        print(f"用户数量: {len(get_json.get('data', []))}")
        if get_json.get('data'):
            print(f"用户列表: {json.dumps(get_json['data'], indent=2, ensure_ascii=False)[:500]}...")
    else:
        print(f"GET失败: {get_resp.text[:200]}")
        
except Exception as e:
    print(f"GET请求异常: {e}")