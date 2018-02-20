# UvA_API_Alumni

- **Dependencies**
  - Python 3.6.0
  - Django 1.11.1
  - See requirements.txt for package dependencies 
  - Note that iPython and its dependencies are not strictly necessary

- **Installation**
  - Install dependencies (assuming Debian based GNU/Linux) `sudo apt install apache2 apache2-dev apache2-utils apache2-mpm-prefork mysql mysql-dev python-dev libapache2-mod-wsgi libffi-dev python-cffi libjpeg-dev zlib1g-dev openssl build-essential libssl-dev`
  - Create virtualenvironment: `virtualenv api_alumni`
  - Activate virtualenv: `source api_alumni/bin/activate`

  - Install required packages: `pip install -r requirements.txt`
  - Setup local_settings: `mv api/api/local_settings.py.example api/api/local_settings.py`
  - Edit local_settings to tailor to your machine.

- **Create directories for the databases, create database and load initial data**
  - **Development**: 
  - `mkdir -p apiweb/databases`
  - `touch apiweb/templates/piwik.html`
  - Create sql dump at production server `mysqldump -u root -p apialumni > ~/sqldump_$(date "+%Y%m%d").sql` (assuming databasename is 'apialumni')
  - Copy database over to local machine, make sure sqlite3 is installed, and that scripts/mysql2sqlite3 is present and executable
  - Convert database to sqlite3 `./scripts/mysql2sqlite3 sqldump_$(date "+%Y%m%d").sql | sqlite3 dev.db`
  - Copy dev.db to apiweb/databases, and setup sqlite3 backend in settings/local.py
  - Alternatively, the data can be dumped using `dumpdata` and loaded using `loaddata`
    - `python manage.py dumpdata --exclude filebrowser --format json --indent 2 >> ~/dump_$(date "+%Y%m%d").json`
    - Copy `~/dump_$(date "+%Y%m%d").json` to local machine, and read-in
    - `python manage.py loaddata ~/dump_$(date "+%Y%m%d").json`
  - **Production**:
  - `mv apiweb/templates/piwik.html.example apiweb/templates/piwik.html`
  - `mysql -u root -p`
    - `CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';`
    - `CREATE DATABASE mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
    - `GRANT ALL PRIVILEGES ON mydatabase.* TO 'user'@'localhost';`
    - `FLUSH PRIVILEGES;`
  - **Both**:
  - `python manage.py makemigrations main alumni survey research interviews`
  - `python manage.py migrate`
  - `python manage.py loaddata apiweb/apps/*/fixtures/*.json`
  - `python manage.py createsuperuser`
  - `python manage.py collectstatic`


- **Create directories for Filebrowser**
  - `mkdir -p apiweb/media/uploads`
  - `mkdir -p apiweb/media/_versions`
  
- **On production only, also set permissions for Apache2**
  - `setfacl -m u::rwx,u:www-data:rwx,g::rwx,o:rx apiweb/databases `
  - `setfacl -d -m u::rwx,u:www-data:rwx,g::rwx,o:rx apiweb/media/uploads`
  - `setfacl -m    u::rwx,u:www-data:rwx,g::rwx,o:rx apiweb/media/uploads`
  - `setfacl -d -m u::rwx,u:www-data:rwx,g::rwx,o:rx apiweb/media/_versions`
  - `setfacl -m    u::rwx,u:www-data:rwx,g::rwx,o:rx apiweb/media/_versions`


- **Copy 2.6GB file with PhD theses**
    - `cp -r path/to/files apiweb/apps/alumni/static/alumni/theses/phd`

- Set unicode things for Python3 to avoid Excel export to break. Not sure which one worked though.
    - Added the following two lines to the bashrc
    - `export LANG='en_US.UTF-8'`
    - `export LC_ALL='en_US.UTF-8'`
    - Added the following line to the apach2 server config `/etc/apache2/apache2.conf`
    - `AddDefaultCharset utf-8`
