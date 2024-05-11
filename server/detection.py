from database import db
import cv2
from ultralytics import YOLO

pet_model = YOLO("./model/best.pt")

classNames = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
]


def image_detection(image_path):
    # --------------------------------추론----------------------------------#
    # 이미지 불러오기
    img = cv2.imread(image_path)
    img = cv2.resize(img, (640, 640))
    """
    # 추론 실행
    if torch.cuda.is_available():  # CUDA 지원하는 gpu(Nvidia gpu)있는 경우 gpu 사용
        results = pet_model.predict(img, device="0")
    else:
        results = pet_model.predict(img, device="cpu")
    # ----------------------------------------------------------------------#
    """
    results = pet_model.predict(img, device="cpu")

    target_count = 0  # number of target plastic bottle

    # 추론 결과 시각화
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            class_name = classNames[cls]
            if class_name in ["2", "4", "6", "8", "10", "12"]:  # target plastic bottle
                target_count += 1
    return target_count
