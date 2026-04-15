from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..services.ocr_service import extract_text

def test_api(request):
    return JsonResponse({"message": "ok"})

@csrf_exempt
def ocr_function(request):
    if request.method == 'POST': 
        image = request.FILES.get('image') 
        if not image: 
            return JsonResponse({'error': '이미지 없음'}, status=400) 
        text = extract_text(image)  
        return HttpResponse(text)