sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled
sudo ln -s /home/box/web/etc/nginx.conf /etc/nginx/conf.d/box.conf
sudo nginx -s reload
sudo ls -lh /etc/nginx/conf.d/

cd /home/box
gunicorn --daemon --bind "0.0.0.0:8080" web.hello:hello

cd /home/box/web/ask
gunicorn --config /home/box/web/etc/gunicorn.conf.py ask.wsgi
