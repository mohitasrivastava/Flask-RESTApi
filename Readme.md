# REST API CRUD Operations with Python-Flask and MySQL (Version-1)

# Download and setup

Step-1: Creating & activating venv
Windows:

```powershell
  python -m venv venv
  ./venv/Scripts/activate
```

Linux:

```bash
  python -m venv venv
  source venv/bin/activate
```

Step-2: Installing Dependencies

```bash
  pip install -r requirements.txt
```

Step-3: Running application
Windows:

''' setting virtual environment development
$env:FLASK_ENV="development"  
 '''
''' $env:PYTHONDONTWRITEBYTECODE=1
This to prevent making of **pycache**file
'''

```bash
  > $env:PYTHONDONTWRITEBYTECODE=1;$env:FLASK_APP="app";$env:FLASK_ENV = "development"
  > flask run
```

Linux:

```bash
  > export PYTHONDONTWRITEBYTECODE=1 FLASK_APP="app" FLASK_ENV="development"
  > flask run
```

# Installing Dependencies

```bash
  pip install -r requirements.txt
```

# Dependenciews are

''' pip install mysql-connector-python
pip install PyJWT
'''

# Common Issues

1. Creating **pycache** files
   Windows-powershell-Solution:

```bash
  $env:PYTHONDONTWRITEBYTECODE=1
```

Linux:

```bash
export PYTHONDONTWRITEBYTECODE=1
```

# Common Errors

1. While activating venv this error occures in Windows:

   ```bash
       + CategoryInfo          : SecurityError: (:) [], PSSecurityException
       + FullyQualifiedErrorId : UnauthorizedAccess
   ```

   Solution:
   Execute this command and retry activating venv.

   ```bash
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   pip freeze > requirement.txt

   pip install -r requirement.txt

   flask run

   ''' uploading File sytem'''
   1.upload file from postman to server
   2.upload a file with a unique filename
   3.updating filepath in DB with respective entity
   4.Creating a filepath to read file
