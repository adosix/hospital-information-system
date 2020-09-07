#!/bin/bash
db_init=`cat db_init.sql`
echo "$db_init"
sudo mysql -u root -e "$db_init"