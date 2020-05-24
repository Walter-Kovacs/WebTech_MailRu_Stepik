sudo apt update
sudo apt install python3.5
sudo apt install python3.5-dev
sudo unlink /usr/bin/python
sudo ln -s /usr/bin/python3.5 /usr/bin/python
sudo python -m pip install --upgrade pip
sudo python -m pip install gunicorn
sudo python -m pip install django==2.0
sudo python -m pip install mysqlclient

sudo rm /etc/nginx/sites-enabled/default
sudo nginx
sudo service mysql start
echo "ATTENTION! Now create 1) web/ask/mysql.conf 2) stepik_ask database 3) ./migrations migrate"
