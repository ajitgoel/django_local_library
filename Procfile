#Procfile declares the application's process types and entry points
#The "web:" tells Heroku that this is a web dyno and can be sent HTTP traffic. 
#The process to start in this dyno is gunicorn(popular web application server that Heroku recommends). 
#We start Gunicorn using the configuration information in the module locallibrary.wsgi(created with our application skeleton: /locallibrary/wsgi.py).
web: gunicorn locallibrary.wsgi --log-file -