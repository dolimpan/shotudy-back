from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.services.learning_service import generate_learning_content

@csrf_exempt
def learning_fubnction(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")

        if not keyword:
            return JsonResponse({"error": "키워드 없음"}, status=400)

        result = generate_learning_content(keyword)
        return JsonResponse(result)