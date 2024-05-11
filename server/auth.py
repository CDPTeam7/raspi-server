# from flask_cors import CORS # CORS 미들웨어를 위한 모듈
from flask import request, jsonify, make_response  # flask 관련 라이브러리
from flask_restx import Resource, Namespace, fields  # Api 구현을 위한 Api 객체 import
import hashlib  # 비밀번호 암호화를 위한 모듈
from tokens import *
from database import db
import os
from dotenv import load_dotenv


# 전처리
Auth = Namespace(
    name="Auth",
    description="login 관련 API",
)
# load .env
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_ALGORITHMS = os.environ.get("JWT_ALGORITHMS")

"""
SECRET_KEY = "b_4(!id8ro!1645n@ub55555hbu93gaia0"  # 테스트용 secret key
JWT_ALGORITHM = "HS256"  # 암호화할 때 쓸 알고리즘
"""


"""auth_check_userinfo_fields = Auth.model(
    "Auth_check_userinfo_request",
    {},
)"""
auth_check_userinfo_response1_data = Auth.model(
    "Auth_check_userinfo_response1_data",
    {
        "nickname": fields.String(example="nick"),
        "point": fields.Integer(example=30),
        "score": fields.Integer(example=120),
        "regionName": fields.String(example="대구"),
        "areaName": fields.String(example="북구"),
    },
)
auth_check_userinfo_response1 = Auth.model(
    "Auth_check_userinfo_success",
    {
        "result": fields.String(example="SUCCESS_CHECK_USER_INFO"),
        "msg": fields.String(example="유저 정보 확인에 성공하였습니다."),
        "data": fields.Nested(auth_check_userinfo_response1_data),
    },
)
auth_check_userinfo_response2 = Auth.model(
    "Auth_check_userinfo_fail1",
    {
        "result": fields.String(example="ERROR_FAIL_CHECK_USER_INFO"),
        "msg": fields.String(example="유저 정보 확인에 실패하였습니다."),
    },
)
auth_check_userinfo_response3 = Auth.model(
    "Auth_check_userinfo_fail2",
    {
        "result": fields.String(example="ERROR_ACCESS_TOKEN_NOT_EXIST"),
        "msg": fields.String(example="access token이 유효하지 않습니다."),
    },
)


# 유저 정보 확인
@Auth.route("/check-userinfo", methods=["GET"])
class api_check_userinfo(Resource):
    # @Auth.expect(auth_check_userinfo_fields)
    @Auth.response(200, "success", auth_check_userinfo_response1)
    @Auth.response(400, "fail", auth_check_userinfo_response2)
    @Auth.response(401, "fail", auth_check_userinfo_response3)
    @token_required
    def get(self):
        """유저 정보를 가져옵니다"""
        payload = get_payload_from_header()
        if payload is None:
            return make_response(
                jsonify({"result": "fail", "msg": "access token이 유효하지 않습니다."}),
                402,
            )
        try:
            id_receive = payload["id"]
            # select 쿼리 실행: request의 name과 동일한 document 찾기
            result = db.user.find_one(
                {"user_id": id_receive},
                {
                    "_id": 0,
                    "nickname": "$nick",
                    "point": 1,
                    "score": 1,
                    "regionName": "$region",
                    "areaName": "$area",
                },
            )
            # 데이터를 처리하고 응답 생성
            response_data = {
                "result": "SUCCESS_CHECK_USER_INFO",
                "msg": "유저 정보 확인에 성공하였습니다.",
                "data": result,
            }
            return make_response(jsonify(response_data), 202)
        except:
            response_data = {
                "result": "ERROR_FAIL_CHECK_USER_INFO",
                "msg": "유저 정보 확인에 실패하였습니다.",
            }
            return make_response(jsonify(response_data), 401)
