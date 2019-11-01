CREATE DATABASE IF NOT EXISTS apiweb;
GRANT ALL PRIVILEGES ON apiweb.* TO 'dbuser'@'%' IDENTIFIED BY 'dbpassword';
GRANT ALL PRIVILEGES ON apiweb.* TO 'dbuser'@'localhost' IDENTIFIED BY 'dbpassword';
FLUSH PRIVILEGES;
