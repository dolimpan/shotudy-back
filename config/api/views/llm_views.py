from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..services.llm_service import analyze_text
import json
@csrf_exempt
def llm_function(request):
    if request.method == 'POST':
        try:
            # 1️⃣ JSON 파싱
            body = json.loads(request.body)
            text = body.get("input123")

            if not text:
                return JsonResponse({'error': 'test 값 없음'}, status=400)

            # 2️⃣ LLM 서비스 호출
            result = analyze_text(text)

            # 3️⃣ JSON 응답
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponse(str(e), status=500)