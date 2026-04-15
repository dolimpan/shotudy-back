import pytesseract
import cv2
import numpy as np

def extract_text(file):
    # 1. 파일 → numpy array
    file_bytes = np.frombuffer(file.read(), np.uint8)
    
    # 2. 이미지 디코딩
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return "이미지 디코딩 실패"

    # 3. 전처리 (성능 핵심🔥)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 노이즈 제거
    gray = cv2.medianBlur(gray, 3)

    # 이진화
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 4. OCR 실행
    text = pytesseract.image_to_string(thresh, lang='kor+eng')

    return text.strip()