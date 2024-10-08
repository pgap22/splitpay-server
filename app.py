import os
from dotenv import load_dotenv
load_dotenv()

from flask_cors import CORS
from flask import Flask
from flask import request
from helper import generate_six_digit_number,get_json_authcode,write_authcode,get_amount,write_amount,get_id_user_amount
import jwt
import socketio 
from prisma import Prisma
from auth_login import authtoken, valid_authtoken
from decimal import Decimal
print(socketio)
db = Prisma()
db.connect()
app = Flask(__name__)
cors = CORS(app)
sio = socketio.AsyncSimpleClient()
io = socketio.SimpleClient()

# Socket.IO server URL
socket_io_server = os.getenv("SOCKETIO_SERVER", 'https://splitq-socket-io.onrender.com/')


async def socketio_connected():
    await sio.connect(socket_io_server)

@app.route("/")
def hello_world():
    return {
        "message": "SplitPay API"
    }

@app.route("/authcode")
def get_auth_code():
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
    
    write_amount(0, request.json['id_user'])

    return {"status": "OK","token": jwt_token}



@app.route("/deposit", methods=["POST"])
async def get_deposit():
    authuser = valid_authtoken(request)
    if('status' in authuser):
        return authuser
    await socketio_connected()
    current_amount = Decimal(str(get_amount()))
    payload_amount = Decimal(str(request.json['value']))
    print(str(current_amount+payload_amount))
    await sio.emit("splitpay-value-deposit", request.json['value'])
    write_amount(float(current_amount+payload_amount), authuser['id_user'])
    await sio.disconnect()
    return {"message": "OK"}

#Actually Dead
# @app.route("/turn-on", methods=["GET"])
# def turn_on():
#     return {"message": "RPI ON"}

# @app.route("/turn-off",methods=["GET"])
# def turn_off():
#     return {"message": "RPI OFF"}

@app.route("/check_authtoken", methods=["POST"])
@authtoken
def check_authtoken(authuser):
    try:
        return {"status": "OK" }
    except Exception as e:
        print(e)
        return {"status": "FAILED", "reason": "SERVER_ERROR"}, 500
    
    
@app.route("/finalize_deposit", methods=['POST'])
@authtoken
def finalize_deposit(authuser):
    try:   
        io.connect(socket_io_server)
        io.emit("splitpay-disconnect")
        id_user = get_id_user_amount()  
        amount = get_amount()
        if(id_user != authuser['id_user']):
            return {"status": "FAILED", "reason": "AUTHCODE_INVALID"}, 401

        if(amount != 0):
            db.recharges.create(data={
                "userID": id_user,
                "balance": amount,
                "type": "splitpay"
                
            })

            db.users.update(data={
                "balance": {
                    "increment": amount
                }
            }, where={
                "id": id_user
            })
        write_amount(0,0)
        io.disconnect()
        return {"status": "OK"}
    except Exception as e:
        print(e)
        return {"status": "FAILED", "reason": "SERVER_ERROR"}, 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)