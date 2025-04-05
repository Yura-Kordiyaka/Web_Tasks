


# Overview
This application helps the user to Read,Create,Delete,Update the Blog post,The app uses django for the server side and React for the client side of the application.

<h3>Feautures:-</h3>
<ul>
<li>Single Page App</li>
<li>Create Post</li>
<li>Read Post</li>
<li>Update Post</li>
<li>Delete Post</li>
</ul>

# Backend-Setup 

Create Virtual env for django-part:-
```
cd Django-React-Blog
virtualenv app
```
Activate Virtual env:-
```
app\scripts\activate
```
Install Dependencies:-
```
cd Backend
pip install -r requirements.txt
```
Make Migrations:-
```
./manage.py makemigrations
./manage.py migrate
```
Start server for your REST-API:-
```
./manage.py runserver
```
# Frontend Setup:-
Go to root and Open another terminal window
```
cd Frontend
```
Install Dependencies:-
```
npm install
```
Run Server:-
```
npm run dev
```
