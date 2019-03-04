FROM nginx:1.15.6-alpine

# Copy Django static files
COPY /eshop/ebag/static /opt/services/djangoapp/static/

# Copy nginx config file
COPY /docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# Chown the static folder to give nginx read permissions on it
RUN chown -R nginx:nginx /opt/services/djangoapp/static
