from helper import get_json_authcode
from functools import wraps
from flask import request
import jwt
import os

def authtoken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Verificar si la solicitud tiene un cuerpo JSON
        if not request.is_json:
            return {"status": "FAILED", "reason": "INVALID_JSON"}, 400

        # Obtener el authtoken de la solicitud
        user_authtoken = request.json.get('authtoken')

        if not user_authtoken:
            return {"status": "FAILED", "reason": "NO_AUTHCODE"}, 400

        try:
            # Decodificar el JWT para obtener el authcode del usuario
            user_authcode = jwt.decode(user_authtoken, key=os.getenv("JWT_SECRET"), algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return {"status": "FAILED", "reason": "TOKEN_EXPIRED"}, 401
        except jwt.InvalidTokenError:
            return {"status": "FAILED", "reason": "INVALID_TOKEN"}, 401

        # Obtener el authcode esperado
        authcode = get_json_authcode()

        # Comparar los authcodes
        if not (authcode == user_authcode.get('splitpay_code')):
            return {"status": "FAILED", "reason": "AUTHCODE_INVALID"}, 400

        # Llamar a la función decorada si todo está bien
        return f(user_authcode, *args, **kwargs)
    return decorated



#For async stuff
def valid_authtoken(request):
     # Verificar si la solicitud tiene un cuerpo JSON
        if not request.is_json:
            return {"status": "FAILED", "reason": "INVALID_JSON"}, 400

        # Obtener el authtoken de la solicitud
        user_authtoken = request.json.get('authtoken')

        if not user_authtoken:
            return {"status": "FAILED", "reason": "NO_AUTHCODE"}, 400

        try:
            # Decodificar el JWT para obtener el authcode del usuario
            user_authcode = jwt.decode(user_authtoken, key=os.getenv("JWT_SECRET"), algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return {"status": "FAILED", "reason": "TOKEN_EXPIRED"}, 401
        except jwt.InvalidTokenError:
            return {"status": "FAILED", "reason": "INVALID_TOKEN"}, 401

        # Obtener el authcode esperado
        authcode = get_json_authcode()

        # Comparar los authcodes
        if not (authcode == user_authcode.get('splitpay_code')):
            return {"status": "FAILED", "reason": "AUTHCODE_INVALID"}, 400
        
        return user_authcode
