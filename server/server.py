# from flask_cors import CORS # CORS 미들웨어를 위한 모듈
from flask import Flask  # flask 관련 라이브러리
from flask_restx import (
    Api,
)  # Api 구현을 위한 Api 객체 import
from tokens import *
from auth import Auth
from point import Point
from ranking import Ranking
from ai_service import Ai_service
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf

# 전처리
app = Flask(__name__)  # flask 객체를 생성. __name__은 현재 실행 중인 모듈 이름
# Flask 객체에 Api 객체 등록
api = Api(
    app,
    version="0.1",
    title="CDPTeam7's API Server",
    description="CDPTeam7's flask API Server",
    doc="/documents/",
    terms_url="/documents/",
    contact="holmane333@naver.com",
    license="MIT",
)
# CORS(app, supports_credentials=True, resources={r'*': {'origins': 'http://localhost:3000'}})  # CORS 미들웨어 추가

# namespace 추가
api.add_namespace(Auth, "/api/auth")
api.add_namespace(Point, "/api/point")
api.add_namespace(Ranking, "/api/rank")
api.add_namespace(Ai_service, "/api/model")


if __name__ == "__main__":  # 이 파일이 직접 실행되야만 해당 코드 실행
    app.run("0.0.0.0", port=8081, debug=True)
