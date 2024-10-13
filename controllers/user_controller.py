
import flask
from flask import request, send_file
from app import app
from models.user_model import user_model
from models.auth_model import auth_model
import os
from datetime import datetime
obj = user_model()
auth = auth_model()
 

@app.route("/user/all", methods = ["GET"])
# The endpoint for token_auth() is automatically getting calculated in the auth_model.token_auth() method
@auth.token_auth()
def all_users():
    # res = flask.Response(obj.all_user_model())
    # res.headers["Content-type"] = "application/json"
    return obj.all_user_model()

@app.route("/user/add", methods=["POST"])
def add_user():
    return obj.add_user_model(request.form)

@app.route("/user/addmultiple", methods=["POST"])
def add_multiple_users():
    return obj.add_multiple_users_model(request.json)

@app.route("/user/delete/<id>", methods=["DELETE"])
def delete_user(id):
    return obj.delete_user_model(id)

@app.route("/user/update", methods=["PUT"])
def update_user():
    return obj.update_user_model(request.form)

@app.route("/user/patch", methods=["PATCH"])
def patch_user():
    return obj.patch_user_model(request.form)

@app.route("/user/page/<pno>/limit/<limit>", methods=["get"])
def pagination(pno, limit):
    return obj.pagination_model(pno, limit)

@app.route("/user/<uid>/avatar/upload", methods=["PATCH"])
def upload_avatar(uid):
    file = request.files['avatar']
    new_filename =  str(datetime.now().timestamp()).replace(".", "") # Epoch Time Generating unique name for the file
    split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
    ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
    ext = split_filename[ext_pos] # Using last index to get the file extension
    db_path = f"uploads/{new_filename}.{ext}"     #saving file into filesystem with unique filename
    file.save(f"uploads/{new_filename}.{ext}")   
    return obj.upload_avatar_model(uid, db_path)

@app.route("/user/avatar/<uid>", methods=["GET"])
def get_avatar(uid):           #creating an endpoint to read file
    data = obj.get_avatar_path_model(uid)
    # return send_file(f"uploads/{filename}")
    root_dir = os.path.dirname(app.instance_path)  
    print(root_dir, "root_dir")
    print(f"{root_dir}/{data['payload'][0]['avatar']}")
    
    return send_file(f"{root_dir}/ {data['payload'][0]['avatar']}")
    
# @app.route("/user/login", methods=["POST"])
# def user_login():
    # auth_data = request.authorization
    # return obj.user_login_model(auth_data['username'], auth_data['password'])
    
@app.route("/user/login", methods=["POST"])
def user_login():
    return obj.user_login_model(request.form)
    
    