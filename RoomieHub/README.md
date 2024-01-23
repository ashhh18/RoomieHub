# Hackathon
This repository is for the members to collaborate and work on the ISS hackathon project.

Team Number: 60

Members:
    1. Ashwin Kumar
    2. Tanay Gad
    3. Vinit Mehta
# Name of Site
ROOMIEHUB
# How to open our website
    -> Run the app.py python file in src folder

# Do:
    -> pip install flask-wtf
    -> pip install email_validator
    -> pip install flask-sqlalchemy
    -> pip install flask-bcrypt
    -> pip install flask-login

# Packages Used
    -> os
    -> secrets
    -> flask
    -> flask_wtf
    -> wtforms
    -> wtforms.validators
    -> flask_wtf.file
    -> wtforms.widgets
    -> flask_sqlalchemy
    -> flask_bcrypt
    -> flask_login
    -> sqlalchemy
    
# Features Implemented
    -> Signin/Signup: 
        Create an account with a unique username and email with the required details.
        Password is initially hidden and can be seen using show password.
    -> Search:  
        Search based on username, and add filters on a variety of parameters.
    -> Profile Page:
        Displays you profile with an option to change details and the people you are are following.
        You can remove people you are following from here.
    -> Followers page:
        Displays people who you follow.
    -> Discover page:
        List of all the users who have registered. 
        

# To create/initiate database run the following command on python inside the shell in the src folder:
    -> from app import app, db
    -> app.app_context().push()
    -> db.create_all()
    -> from app import User
        

# File structure:
    .
    ├── README.md
    └── src
        ├── app.py
        ├── instance
        │   └── database.db
        ├── __pycache__
        │   └── app.cpython-310.pyc
        ├── static
        │   ├── CSS
        │   │   ├── about.css
        │   │   ├── all-users.css
        │   │   ├── discover.css
        │   │   ├── form.css
        │   │   ├── header-footer.css
        │   │   ├── index.css
        │   │   ├── other-user.css
        │   │   ├── profile-page.css
        │   │   ├── search.css
        │   │   ├── signin.css
        │   │   ├── signup.css
        │   │   └── user-info.css
        │   └── Media
        │       ├── ashwin.png
        │       ├── full_logo-no-bg.png
        │       ├── full_logo.png
        │       ├── just_logo-no-bg.png
        │       ├── just_logo.png
        │       ├── main_wp.jpg
        │       ├── profile_pictures
        │       │   ├── 0ef4cb7163bdc70f.png
        │       │   ├── 12d15379b2602609.png
        │       │   ├── 142fec9fa8f58158.png
        │       │   ├── 1584b0cff4219b1a.png
        │       │   ├── 15f1a258c768a426.png
        │       │   ├── 580523b131480055.png
        │       │   ├── 67e91d31c1852e94.png
        │       │   ├── 78ae71f94e1ac827.png
        │       │   ├── 795c35ab97a82f3b.png
        │       │   ├── b61d2d014c664b7c.png
        │       │   ├── ca47999de1bc3628.png
        │       │   ├── ccedd7f63e9d7042.png
        │       │   ├── ccf909394c410b65.png
        │       │   ├── d664d3de7707810e.png
        │       │   ├── default.jpg
        │       │   ├── eec7c6f2a1d5523b.png
        │       │   └── fe7f43479496fac2.png
        │       ├── right.png
        │       ├── tanay.png
        │       ├── vinit.png
        │       └── wrong.png
        └── templates
            ├── Forms
            │   ├── signInEmail.html
            │   ├── signUp.html
            │   └── update.html
            ├── Layouts
            │   ├── form-layout.html
            │   └── main-layout.html
            └── Main-Pages
                ├── about.html
                ├── all-users.html
                ├── discover.html
                ├── followers.html
                ├── index.html
                ├── other-user.html
                ├── profiles.html
                ├── search-page.html
                └── UserInfo.html
