from utils.openai_utils import call_openai

print("🧪 OpenAI 응답 테스트 중...")
response = call_openai("새로 만든 보드게임의 설명 스크립트를 만들어줘.")
print("📨 응답 결과:")
print(response)