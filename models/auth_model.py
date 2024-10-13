from datetime import datetime, timedelta
from logging import exception
import mysql.connector
import jwt
from flask import make_response, request, json
import re
from configs.config import dbconfig
from functools import wraps

class auth_model():
    
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
        
    def token_auth(self, endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                print(endpoint,'endpoint')
                try:
                    authorization = request.headers.get("authorization")
                    if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                        token = authorization.split(" ")[1] #to fetch only token part
                        try:
                            tokendata = jwt.decode(token, "Sagar@123", algorithms="HS256") #To decrypt the token. "Sagar@123" is encryption key will be taken from browser
                        except Exception as e:
                            return make_response({"ERROR":str(e)}, 401)
                        print(tokendata, "tokendata")
                        current_role = tokendata['payload']['role_id']
                        self.cur.execute(f"SELECT * FROM accessbility_view WHERE endpoint='{endpoint}'")
                        result = self.cur.fetchall()
                        print(result,"result")
                        if len(result)>0:
                            roles_allowed = json.loads(result[0]['roles']) #loads Converts List to dictionary
                            print(roles_allowed,"roles_allowed")
                            if current_role in roles_allowed:
                                return func(*args)
                            else:
                                return make_response({"ERROR":"INVALID_ROLE"}, 422)
                        else:
                            return make_response({"ERROR":"INVALID_ENDPOINT"}, 404)
                    else:
                        return make_response({"ERROR":"INVALID_TOKEN"}, 401)
                except Exception as e:
                    return make_response({"ERROR":str(e)}, 401)
            return inner2
        return inner1
    

#To create accessibility_view
# SELECT endpoints.endpoint,
# accessbility.roles
# FROM endpoints join accessbility
# where endpoints.id = accessbility.endpoint_id;