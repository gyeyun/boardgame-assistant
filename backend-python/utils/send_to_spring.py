# utils/send_to_spring.py

import requests
import os

# 예시: 환경변수에서 기본 Spring 서버 주소를 가져옴
SPRING_BASE_URL = os.getenv("SPRING_BASE_URL", "http://localhost:8080")

def send_to_spring(endpoint: str, payload: dict):
    """
    Spring 백엔드로 데이터를 POST 전송하는 함수
    :param endpoint: /api/... 형식의 경로
    :param payload: JSON 데이터 (dict)
    """
    url = SPRING_BASE_URL + endpoint

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"[✔] Spring 서버 응답: {response.status_code}")
    except requests.RequestException as e:
        print(f"[❌] Spring 서버 전송 실패: {e}")
