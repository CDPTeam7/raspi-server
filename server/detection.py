from deepface import DeepFace
from database import db
import math
import cv2
from ultralytics import YOLO
import torch

pet_model = YOLO("./server/model/best.pt")

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


# target image의 embedding 정보 얻기
def get_target_embedding(target_img_path):
    try:
        facial_representations = DeepFace.represent(
            img_path=target_img_path,
            model_name="Facenet512",
            enforce_detection=True,
            detector_backend="fastmtcnn",
        )
        # print(facial_representations)
        if len(facial_representations) == 1:
            target_embedding = facial_representations[0]["embedding"]
        else:
            biggest_face = facial_representations[0]
            for face in facial_representations:
                face_area = face["facial_area"]["w"] * face["facial_area"]["h"]
                if face_area > (
                    biggest_face["facial_area"]["w"] * biggest_face["facial_area"]["h"]
                ):
                    biggest_face = face
            target_embedding = biggest_face["embedding"]

        return target_embedding
    except Exception as e:
        print(e)
        return None


def search_similar_images(target_embedding):
    result = db.image.aggregate(
        [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "image",
                    "queryVector": target_embedding,
                    "numCandidates": 50,
                    "limit": 3,
                }
            }
        ]
    )

    return result


def verify(target, candidate):
    result = DeepFace.verify(
        img1_path=target,
        img2_path=candidate,
        model_name="ArcFace",
        detector_backend="opencv",
        distance_metric="cosine",
        enforce_detection=True,
        align=True,
        expand_percentage=0,
        normalization="base",
        silent=False,
    )

    return result["verified"]
