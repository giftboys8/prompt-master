import requests
import json

def test_dify_api():
    base_url = "http://10.118.0.144/v1"
    api_key = "app-rzz0BZyhFdoqgGam35KCHSVW"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": "Hello, this is a test message",
        "user": "test_user",
        "response_mode": "blocking",
        "inputs": {}  # 添加空的inputs参数
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat-messages",
            headers=headers,
            json=data
        )
        
        print("Status Code:", response.status_code)
        print("Response Headers:", json.dumps(dict(response.headers), indent=2))
        print("Response Body:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    test_dify_api()