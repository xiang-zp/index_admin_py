import requests
import json

# 简单的测试脚本
print("测试创建用户API")

# 1. 登录
login_url = "http://localhost:8000/api/auth/admin/login"
login_data = {"username": "admin", "password": "admin123"}

print("登录...")
resp = requests.post(login_url, json=login_data)
print(f"登录响应: {resp.status_code}")

if resp.status_code == 200:
    token = resp.json()["data"]["token"]
    print(f"Token: {token[:30]}...")
    
    # 2. 创建用户
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    create_data = {
        "username": "testuser123",
        "password": "test123",
        "role": "editor"
    }
    
    print("\n创建用户...")
    create_resp = requests.post("http://localhost:8000/api/admin/users/", 
                                json=create_data, headers=headers)
    
    print(f"创建用户响应状态: {create_resp.status_code}")
    print(f"创建用户响应体: {create_resp.text}")
    
    # 3. 检查响应结构
    if create_resp.text:
        try:
            data = create_resp.json()
            print(f"\n响应JSON结构:")
            for key, value in data.items():
                print(f"  {key}: {type(value).__name__}")
                if key == "data" and value:
                    print(f"    data内容: {value}")
        except:
            print("响应不是JSON")
else:
    print("登录失败")