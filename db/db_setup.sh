#!/bin/bash

db_cleanup=`cat db_cleanup.sql`
echo "$db_cleanup"
sudo mysql -u root -e "$db_cleanup"
db_init=`cat db_init.sql`
echo "$db_init"
sudo mysql -u root -e "$db_init"
fill_data=`cat fill_data.sql`
echo "$fill_data"
sudo mysql -u root -e "$fill_data"
