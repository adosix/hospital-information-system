# Hospital information system

Instalation:
###We will install all prerequisites by following commands
sudo apt install python3-pip

pip3 install virtualenv

###Create virtual environment

###installprerequisites to environment

sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip3 install mysqlclient

###after that we will login as root
sudo mysql -u root

###create database
CREATE DATABASE hospital_data;

###create django user and give him priviledges
CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL ON hospital_data.* TO 'djangouser'@'%';
FLUSH PRIVILEGES;

###libraries for our django application
pip3 install django-multiforloop
pip3 install django-crispy-forms

###run django localy
./start
