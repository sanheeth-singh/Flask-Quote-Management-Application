BunnyMe9 Quotes and Notes Web Application
This project is a Flask-based web application that allows users to register, log in, and manage personal notes along with viewing random quotes. It demonstrates core web development concepts such as authentication, database integration, form handling, and clean UI design using Flask and related extensions.
The project is intended for learning, practice, and portfolio demonstration.

◽Project Overview

The application provides:

-User authentication using Flask-Login

-Secure form handling using Flask-WTF

-Database operations using SQLAlchemy

-CRUD functionality for notes

-Quote display on the homepage

-Flash messages for user feedback

-Session-based user experience

-Each user can create, edit, delete, and search their own notes after logging in


◽Features

1)Authentication

User registration with unique username validation

User login and logout

Session handling using Flask-Login

Account deletion support

2)Quotes Management

Create new quotes

Edit existing quotes

Delete quotes

Notes are linked to individual users

3)Quotes

Random quote displayed on the homepage

Refresh quote without reloading the entire app

4)User Interface

Bootstrap-based layout

Gradient header design

Responsive pages

Flash messages for errors and success notifications


◽Technology Stack

Python 3

Flask

Flask-Login

Flask-WTF

Flask-SQLAlchemy

WTForms

SQLite

HTML, CSS, Bootstrap


◽Project Structure

App-flask1/

├── testflaskapp.py

├── models.py

├── forms.py

├── README.md

├── requirements.txt

├── .gitignore

├── instance/

│   └── app.db

├── templates/

│   ├── base.html

│   ├── home.html

│   ├── login.html

│   ├── register.html

│   ├── changes.html

│   ├── preferences.html

│   ├── view.html

│   ├── test_delete.html

│   └── edit_note.html

└── static
    ├── css
    └── images


◽Database

The application uses SQLite for local development. The database file is created automatically when the app is run for the first time.

Delete the existing project db to start fresh.


◽Future Improvements

Password reset functionality

User profile page

Tags and categories for notes

REST API support

Deployment to cloud platforms

Improved search and filtering


◽Author

Developed by Sanheeth Singh

Flask-based learning and portfolio project

