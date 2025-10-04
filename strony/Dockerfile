FROM php:8.2-apache

# Instalacja rozszerzeń PHP dla MySQL
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Włącz moduł Apache rewrite (opcjonalnie)
RUN a2enmod rewrite

WORKDIR /var/www/html
