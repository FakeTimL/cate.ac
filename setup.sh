#!/bin/sh

# Set environment variables first.
# See `drp49_secret.txt`.

# MySQL setup commands:
#
# ```sh
# $> sudo mysql_secure_installation
# $> sudo mysql -u root [-p]
#
# mysql> CREATE USER 'drp49_db'@'localhost' IDENTIFIED BY '[DRP49_MYSQL_PASSWORD]';
# mysql> CREATE DATABASE drp49_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;
# mysql> GRANT ALL PRIVILEGES ON drp49_db.* TO 'drp49_db'@'localhost';
# mysql> EXIT;
#
# $> sudo systemctl enable mysql
# $> sudo systemctl start mysql
# ```

# Python setup commands:
#
# ```sh
# $> pip install virturalenv
# $> virtualenv env
# $> . env/bin/activate
# $> pip install -r requirements.txt
# ```

# Nginx setup commands:
#
# ```sh
# $> sudo cp nginx.conf /etc/nginx/nginx.conf
# $> sudo systemctl enable nginx
# $> sudo systemctl start nginx
# ```

python3 manage.py collectstatic
python3 manage.py migrate

# Running/restarting server:
#
# ```sh
# $> . env/bin/activate
# $> ./run.sh
# ```

# Domains: drp49.dev www.drp49.dev cate.ac www.cate.ac
#
# ```sh
# sudo certbot certonly --nginx
# ```
