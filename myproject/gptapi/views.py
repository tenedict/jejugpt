from openai import OpenAI
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
from dotenv import load_dotenv








load_dotenv()

# # OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class GPTAPIView(APIView):
    def post(self, request):
        # 클라이언트로부터 받은 prompt 값
        prompt = request.data.get("prompt", "")
        
        # prompt 값이 없는 경우
        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4",  # 최신 GPT 모델
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,  # 응답의 최대 토큰 수
                temperature=0.5,  # 창의성 조정
            )
            
            # 응답 메시지 추출
            message = response.choices[0].message.content
            return Response({"response": message}, status=status.HTTP_200_OK)
            
        except Exception as e:
            # 에러 처리
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
