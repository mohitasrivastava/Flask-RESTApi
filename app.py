from flask import Flask

app = Flask(__name__)

try:
    from controllers import *       #this will treat as python package
except Exception as e:
    print(e)

# OR from controllers import user_controller, product_controller     #this will treat as python file




