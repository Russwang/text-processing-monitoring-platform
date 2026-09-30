FROM php:8.3-apache
COPY src/ /var/www/html/

RUN sed -i 's/80/100/g' /etc/apache2/ports.conf
RUN sed -i 's/:80/:100/g' /etc/apache2/sites-enabled/000-default.conf
EXPOSE 100
