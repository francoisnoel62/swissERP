# swissERP

Proudly deployed on ![Heroku](https://pyheroku-badge.herokuapp.com/?app=swiss-erp&style=flat)

swissERP aims to be an easy business software for invoices and payments.

Check this project online [here](https://swiss-erp.herokuapp.com/)


# Introduction


![Landing page](static/landing/images/header-hero.png)

### Main features

* Separated dev and production settings (currently deployed on Heroku)

* Example app with custom user model

* User registration and logging in as demo

* Procfile for easy deployments

* SQLite by default if no env variable is set (DEBUG == True)

      
### No virtualenv

This assumes that `python3` is linked to valid installation of python3 and that `pip` is installed and `pip3`is valid
for installing python3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.

If you don't have django installed for python3, then run:

    $ pip3 install django
    
And then:

    $ python3 -m django startproject \
      --template=https://github.com/francoisnoel62/swissERP/tree/master \
      --extension=py,md \
      <project_name>
      
      
After that : just install the local dependencies, run migrations, and start the server.


# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/francoisnoel62/swissERP.git
    $ cd {{ project_name }}
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
