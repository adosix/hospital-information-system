#!/bin/bash
if [ $1 == "dbinit" ] 
then
    db_cleanup=`cat db/db_cleanup.sql`
    echo "enter django user password"
    mysql -u djangouser -p -e "$db_cleanup" 
    echo "db_cleanup done"

    db_init=`cat db/db_init.sql`
    echo "enter django user password"
    mysql -u djangouser -p -e "$db_init"
    echo "db_init done"

    fill_data=`cat db/fill_data.sql`
    echo "enter django user password"
    mysql -u djangouser -p -e "$fill_data"
    echo "db_fill_data done"
fi
#activate virtual environment
#source ../Environments/hospital_env/bin/activate
#check for changes and run server
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

