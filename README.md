# UvA_API_Alumni

- **Dependencies**
  - Python 3.8.2
  - Django 2.2.11
  - See requirements.txt for package dependencies 
  - Note that iPython and its dependencies are not strictly necessary

- **Installation (Option 1)**
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

## **Alternatively, run with Docker (Option 2)**
- Make sure Docker Engine and docker-compose are installed 
  (see [Docker docs](https://docs.docker.com/install/))

### **Running with Django's built-in development server w/ sqlite3 database (Option 2a)**
- Build the image: `docker build -t apiweb .`
- Setup local settings: `cp apiweb/settings/.env.example apiweb/settings/.env`
- Edit `settings/.env` to tailor to your machine.
- TODO: command below misses a considerable number of volumes linked into the container. See `docker-compose.yml`
- Run the server: `docker run --rm -it -v "$(pwd)/apiweb/settings/.env:/apiweb/settings/.env" -v "$(pwd)":/apiweb -p 1337:1337 
  --name runserver apiweb bash -c "python manage.py runserver 0.0.0.0:1337"` (and leave running)
  - Visit the website at http://localhost:1337
- In a new terminal, one can execute commands in the running container. Load the fixtures:
  - `docker exec runserver bash -c "python manage.py loaddata apps/*/fixtures/*.json"`
- In a new terminal, one can attach to the container in an interactive session:
  - `docker exec -it runserver bash`

### **Running the full stack: nginx + uwsgi w/ mariadb (mysql) database (Option 2b)**
- `./nginx/generate_sslcert.sh`
- `docker-compose up -d mariadb`
  - On first launch, the database and user will be created (you don't have to do anything)
- `docker-compose build django nginx`
- `docker-compose up --build`
- In a new terminal, one can attach to the container in an interactive session:
  - `docker exec -it apiweb bash`
- Now add the initial data (run this command in the container!)
  - `python manage.py loaddata apps/*/fixtures/*.json` 
- Create a superuser (run this command in the container)
  - `python manage.py createsuperuser`
- Visit the website at https://localhost (and accept the self-signed 
  certificate warning of the browser)
