Project 4: Item catalog
====================================
This project is about building a fully functional application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

# Installation
First, either clone or download the project code from this repo:

#### Cloning using SSH or HTTPS
```
$ git clone git@github.com:suffianhamzah/udacity-fsnd-project4.git
```

#### Installing requirements
In order to run this project, you would need to install a list of modules located in ```requirements.txt```.

If using virtualenv:
```
  $ pip install -r requirements.txt
```
If not:
```
 $ sudo pip install -r requirements.txt  # Caution, this will install modules globally.
```

# Setting up API keys, and database

#### Setting up Google API
This web app uses Google as a third-party provider for oauth authentication and authorization. You will need to set up a Google API key in the environment variable.

You can obtain the API from [Google Developer website](https://developers.google.com/)
Then, you would need to set an evironment variable, 'GOOGLE_API'.

#### Getting the data for the database:
```
  $ python manage.py createdb
```

# Usage

To run this project, type: ```python manage.py runserver```

