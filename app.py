import os
from dotenv import load_dotenv
load_dotenv()

from flask_cors import CORS
from flask import Flask
from flask import request
from helper import generate_six_digit_number,get_json_authcode,write_authcode,get_amount,write_amount
import time
import jwt
import socketio
import asyncio

app = Flask(__name__)
cors = CORS(app)
sio = socketio.AsyncSimpleClient()
async def socketio_connected():
    await sio.connect(f"{os.getenv("SOCKETIO_SERVER")}")

@app.route("/")
def hello_world():
    return {
        "message": "SplitPay API"
    }

@app.route("/authcode")
def get_auth_code():
    time.sleep(2)
    authcode =  generate_six_digit_number()
    write_authcode(authcode)
    return {
        "code": authcode
    }

@app.route("/auth", methods=["POST"])
def auth():
    authcode = get_json_authcode()

    #TODO MAKE A DICTIONARY WITH ERROR CODES AND STATUS 

    if(('authcode' in request.json) is not True):
        return {"status": "FAILED", "reason": "NO_AUTHCODE"},400
    if(('id_user' in request.json) is not True):
        return {"status": "FAILED", "reason": "NO_ID_USER"},400

    if(authcode!=request.json['authcode']):
        return {"status": "FAILED", "reason": "AUTHCODE_INVALID"}, 401
    

    jwt_token = jwt.encode(
                    {"splitpay_code": str(authcode), "id_user": request.json['id_user']},
                    os.getenv("JWT_SECRET"),
                    algorithm="HS256"
    )
    
    return {"status": "OK","token": jwt_token}


@app.route("/deposit", methods=["POST"])
async def get_deposit():
    current_amount = get_amount()
    time.sleep(2)
    await socketio_connected()
    data = float(request.json['value'])
    write_amount(data+current_amount)
    await sio.emit("splitq-value", data)
    await sio.disconnect()
    return {"message": "OK"}