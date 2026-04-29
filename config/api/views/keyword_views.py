from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.services.keyword_service import extract_keyword

@csrf_exempt
def keyword_function(request):
    if request.method == "POST":
        text = request.POST.get("text")

        if not text:
            return JsonResponse({"error": "텍스트 없음"}, status=400)

        result = extract_keyword(text)
        return JsonResponse(result)