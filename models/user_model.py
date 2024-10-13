from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import json
from flask import make_response, jsonify
import jwt
from configs.config import dbconfig


class user_model():
    def __init__(self):    #Constructor for Connection establishment b/w python and Mysql  
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.con.autocommit=True     #For insert Query we have to commit
            self.cur = self.con.cursor(dictionary=True)   #Constructor for Query Execution #Cursor to DML operations
        except:
            print("Error")
    def all_user_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)  #dumps stringify
            # return {"payload":result}
            return make_response({"payload":result},200)
        else:
            return "No Data Found"
    
    def add_user_model(self,data):
          
        try:
            print("Hii")
            qry = f"INSERT INTO users(name, email, phone, role_id, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role_id']}', '{data['password']}')"
            print(qry)
            self.cur.execute(qry)
            return make_response({"message":"CREATED_SUCCESSFULLY"},201)
        except Error as e:
               print(e, "hhghghh")
               return "error found"
        
    def add_multiple_users_model(self, data):
        # Generating query for multiple inserts
        qry = "INSERT INTO users(name, email, phone, role_id, password) VALUES "
        for userdata in data:
            qry += f" ('{userdata['name']}', '{userdata['email']}', '{userdata['phone']}', {userdata['role_id']},'{userdata['password']}'),"
        finalqry = qry.rstrip(",")
        self.cur.execute(finalqry)
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def delete_user_model(self,id):
       try:
          print(id, "id")
          self.cur.execute(f"DELETE FROM users WHERE id={id}")
          if self.cur.rowcount>0:
            return make_response({"message":"DELETED_SUCCESSFULLY"},202)
          else:
            return make_response({"message":"CONTACT_DEVELOPER"},500)
       except Error as e:
               print(e, "hhghghh")
               return "error found"
           
    #PUT replaces an entire resource
    def update_user_model(self,data):
        try:
            print(data, "data")
            self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}' WHERE id={data['id']}")
            if self.cur.rowcount>0:
               return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
            else:
               return make_response({"message":"NOTHING_TO_UPDATE"},204)
        except Error as e:
               print(e, "hhghghh")
               return "error found"
    #PATCH updates only specific fields of a resource    
    def patch_user_model(self, data):
        qry = "UPDATE users SET "
        for key in data:
            if key!='id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {data['id']}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def pagination_model(self, pno, limit):
        pno = int(pno)
        limit = int(limit)
        start = (pno*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"page":pno, "per_page":limit,"this_page":len(result), "payload":result})
        else:
            return make_response({"message":"No Data Found"}, 204)

    def upload_avatar_model(self, uid, db_path):
        try: 
           self.cur.execute(f"UPDATE users SET avatar='{db_path}' WHERE id={uid}")  #uploading file from postman to server
           if self.cur.rowcount>0:
              return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":db_path},201)
           else:
               return make_response({"message":"NOTHING_TO_UPDATE"},204)
        except Error as e:
               print(e, "hhghghh")
               return "error found"
        
    def get_avatar_path_model(self, uid):
        
        try: 
            print(uid, "uid")   
            self.cur.execute(f"SELECT avatar FROM users WHERE id={uid}")
            result = self.cur.fetchall()
        
            if len(result)>0:
                print(type(result))
                print(result, "re")
                return {"payload":result}
            else:
                return "No Data Found"  
        except Error as e:
               print(e, "hhghghh")
               return "error found"
        
    def user_login_model(self, data):
        print(data, "data")
        self.cur.execute(f"SELECT id, role_id, avatar, email, name, phone from users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        print(result,"re")
        if len(result)==1:
            exptime = datetime.now() + timedelta(minutes=15) # setting expiration time after 15 min.
            exp_epoc_time = exptime.timestamp() #calculating epoch time which includes expiration
            data = {
                "payload":result[0],  #list of Dictionary. So, 0index
                "exp":int(exp_epoc_time)
            }
            print(int(exp_epoc_time))
            jwt_token = jwt.encode(data, "Sagar@123", algorithm="HS256")  #Generating Encryption key of particular user
            return make_response({"token":jwt_token}, 200)
        else:
            return make_response({"message":"NO SUCH USER"}, 204)
            

            
   