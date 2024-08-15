import random
import json

def write_json(json_file="code.json", data={}):
   with open(json_file, 'w') as f:
    json.dump(data, f, ensure_ascii=False)

def read_json(json_file="code.json"):
   f = open(json_file)
   data = json.load(f)
   return data

def write_authcode(authcode):
   write_json(data={"authcode": str(authcode)})
   return "Success"

def get_json_authcode():
   return read_json()['authcode']

def generate_six_digit_number():
    return random.randint(100000, 999999)

def write_amount(amount, id):
   write_json(json_file="amount.json", data={"amount": amount, "id_user": id})

def get_amount():
   return read_json(json_file="amount.json")['amount']
def get_id_user_amount():
   data = read_json(json_file="amount.json")['id_user']
   return data