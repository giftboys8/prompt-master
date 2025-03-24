#!/usr/bin/env python
"""
提示词管家API测试脚本
"""
import requests
import json
import sys
from urllib.parse import urljoin

class APITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def _url(self, endpoint):
        return urljoin(self.base_url, endpoint)
    
    def _print_response(self, response, endpoint):
        print(f"\n{'='*50}")
        print(f"测试: {endpoint}")
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {response.elapsed.total_seconds():.3f}秒")
        try:
            print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        except:
            print(f"响应内容: {response.text[:200]}...")
        print(f"{'='*50}\n")
        return response.status_code
    
    def register(self, username, email, password):
        """测试用户注册"""
        endpoint = "/api/v1/auth/register/"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = requests.post(self._url(endpoint), json=data, headers=self.headers)
        return self._print_response(response, endpoint)
    
    def login(self, username, password):
        """测试用户登录并获取令牌"""
        endpoint = "/api/v1/auth/token/"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(self._url(endpoint), json=data, headers=self.headers)
        if response.status_code == 200:
            self.token = response.json().get("access")
            self.headers["Authorization"] = f"Bearer {self.token}"
        return self._print_response(response, endpoint)
    
    def get_user_info(self):
        """测试获取用户信息"""
        endpoint = "/api/v1/users/info/"
        response = requests.get(self._url(endpoint), headers=self.headers)
        return self._print_response(response, endpoint)
    
    def get_templates(self):
        """测试获取模板列表"""
        endpoint = "/api/v1/templates/templates/"
        response = requests.get(self._url(endpoint), headers=self.headers)
        return self._print_response(response, endpoint)
    
    def get_scenes(self):
        """测试获取场景列表"""
        endpoint = "/api/v1/scenes/"
        response = requests.get(self._url(endpoint), headers=self.headers)
        return self._print_response(response, endpoint)
    
    def get_contents(self):
        """测试获取内容列表"""
        endpoint = "/api/v1/contents/"
        response = requests.get(self._url(endpoint), headers=self.headers)
        return self._print_response(response, endpoint)
    
    def get_api_keys(self):
        """测试获取API密钥列表"""
        endpoint = "/api/v1/api-keys/"
        response = requests.get(self._url(endpoint), headers=self.headers)
        return self._print_response(response, endpoint)
    
    def get_frameworks(self):
        """测试获取框架列表"""
        endpoint = "/api/v1/admin/frameworks/"
        response = requests.get(self._url(endpoint), headers=self.headers)
        return self._print_response(response, endpoint)
    
    def run_all_tests(self):
        """运行所有测试"""
        # 测试注册和登录
        username = "test_user"
        email = "test@example.com"
        password = "Test@123456"
        
        print("开始API测试...\n")
        
        # 注册新用户(可能会失败如果用户已存在)
        self.register(username, email, password)
        
        # 登录
        login_status = self.login(username, password)
        if login_status != 200:
            print("登录失败，无法继续测试需要认证的API")
            return False
        
        # 测试各种API端点
        self.get_user_info()
        self.get_templates()
        self.get_scenes()
        self.get_contents()
        self.get_api_keys()
        self.get_frameworks()
        
        print("API测试完成!")
        return True

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    tester = APITester(base_url)
    tester.run_all_tests()