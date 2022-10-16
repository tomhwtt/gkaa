server {
  listen 80;
  server_name imagecrazy.com

  location / {
    return 301 https://$host$request_uri;
  }

}

server {
  listen 443 ssl;
  server_name imagecrazy.com

  ssl_certificate       /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
  ssl_certificate_key   /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

  location /static {
    alias /vol/static;
  }

  location / {
    uwsgi_pass              ${APP_HOST}:${APP_PORT};
    include                 /etc/nginx/uwsgi_params;
    client_max_body_size   10M;
  }
}
