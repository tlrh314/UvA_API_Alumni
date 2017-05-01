# UvA_API_Alumni

- **Dependencies**
  - Python 3.6.0
  - Django 1.11
  - See requirements.txt for package dependencies 
  - Note that iPython and its dependencies are not strictly necessary

- **Installation**
  - Create virtualenvironment: `virtualenv api_alumni`
  - Activate virtualenv: `source api_alumni/bin/activate`

  - Install required packages: `pip install -r requirements.txt`
  - Setup local_settings: `mv api/api/local_settings.py.example api/api/local_settings.py`
  - Edit local_settings to tailor to your machine.



# [TODO:] Deployment 
** Copied from Waterman /home/martin/Websites/Configurations/Howto-apiweb3.txt ** 

Make an account on https://bitbucket.org/

bitsmartie/XXXXXXX

Make a fork of the apiweb/apiweb repository managed by Evert, which becomes bitsmartie/apiweb.
We upload a public ssh-key to bitbucket, which makes it easier to push a develop branch later.

On waterman we clone this repository.

cd /home/martin/Websites
git clone https://bitbucket.org:/bitsmartie/apiweb apiweb3

Cloning into 'apiweb3'...
Username for 'https://bitbucket.org:': bitsmartie
Password for 'https://bitsmartie@bitbucket.org:': 
remote: Counting objects: 3256, done.
remote: Compressing objects: 100% (1435/1435), done.
remote: Total 3256 (delta 1679), reused 3176 (delta 1606)
Receiving objects: 100% (3256/3256), 97.13 MiB | 22.90 MiB/s, done.
Resolving deltas: 100% (1679/1679), done.
Checking connectivity... done.

origin automatically points to the bitbucket fork: it is the origin of the clone

martin@waterman:~/Websites/apiweb3$ git remote -v
origin    https://bitbucket.org:/bitsmartie/apiweb (fetch)
origin    https://bitbucket.org:/bitsmartie/apiweb (push)

We tell git to set an upstream (remote) to the original repository.

git remote add upstream https://bitbucket.org:/apiweb/apiweb

martin@waterman:~/Websites/apiweb3$ git remote -v
origin      https://bitbucket.org:/bitsmartie/apiweb (fetch)
origin      https://bitbucket.org:/bitsmartie/apiweb (push)
upstream  https://bitbucket.org:/apiweb/apiweb (fetch)
upstream  https://bitbucket.org:/apiweb/apiweb (push)


git checkout -b develop
Switched to a new branch "develop"

This is shorthand for:

$  git branch   develop
$  git checkout develop

To update your local master with a remote master:
$  git status
$  git checkout master
$  git fetch upstream
$  git status
$  git merge upstream/master
$  git status
$  git push origin master
$  git status

To delete a local branch and a remote branch:
$  git branch -d develop
Deleted branch develop (was 053128f).
$  git push origin :develop
Username for 'https://bitbucket.org:': bitsmartie
Password for 'https://bitsmartie@bitbucket.org:': 
To https://bitbucket.org:/bitsmartie/apiweb
 - [deleted]         develop



[develop e24954d]  Added filebrowser to requirements.txt
 Committer: Martin Heemskerk <martin@waterman.science.uva.nl>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 1 file changed, 4 insertions(+)

git commit --amend --author="Author Name <email@address.com>"

---------------------------------------------------------------------------------------------


== Install the necessary packages and Python stuff ====

On Ubuntu 14.04, with Python 3.4

Ubuntu packages:
- python3-dev
- python3-pip


==== Using virtualenv ====

Python 3.4 on Ubuntu 14.04 has a problem, in the sense that it can’t set up a
simple virtual environment itself. Therefore, install virtualenv explicitly through pip:

  $ pip3 install virtualenv

Check that the virtualenv you’ve installed and are using is the one that comes with Python 3 
(look at the first line of the executable script).
If not, there is a --python option to point it to the right python version.

Create and/or cd into a directory where you want your virtual environments stored.
e.g: /home/martin/Websites/Virtualenvs
From there, set up an apiweb3 virtualenv:

    $ virtualenv apiweb3 --always-copy --python=/usr/bin/python3.4
or 
    $ virtualenv apiweb3 --always-copy

The --always-copy flag copies the complete Python executable and its libraries into your virtualenv.
That avoids potential complications in case of upgrades.

You then activate the virtualenv by sourcing the activate file in the virtualenv bin directory:

For bash:

    $ . apiweb3/bin/activate

For csh:

    $ source apiweb3/bin/activate.csh

Generally, your command prompt will change to reflect you’re using a virtualenv. 
Check your Python and pip executables:

    $ which python
    $ which pip

Now you can safely “pip install” things (with --prefix or --user flags), 
which will all be stored inside the virtualenv apiweb3 directory.

First upgrade pip in the virtualenv:
pip install --upgrade pip
(You are using pip version 7.1.0, however version 8.0.2 is available.
 You should consider upgrading via the 'pip install --upgrade pip' command.)


Obtain the source for apiweb (as described above). 
Change to the root directory: this is the directory with manage.py and requirements.txt. 
Then:

  $ pip install -r requirements.txt

This should install all the necessary Python packages.
Ensure that the ‘pip’ you’re using is the correct pip for your python 3 version.

[Successfully installed Django-1.9.4 Markdown-2.6.5 Pillow-3.1.1 django-filebrowser-no-grappelli 
 flickrapi-2.1.2 oauthlib-1.0.3 pytz-2015.7 reportlab-3.3.0 requests-2.9.1 requests-oauthlib-0.6.1 
 requests-toolbelt-0.6.0 six-1.10.0]


To stop working in the virtualenv, just run 

    $ deactivate


When compiling mod_wsgi, simply use this Python 
(which should be the same as the system python3 anyway).
When using mod_wsgi + apache, you just adjust the WSGIPythonPath. 
See e.g. https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/#using-a-virtualenv


==== Compiling and using mod wsgi for Python 3 ===

Every Python version (x.y) should have its own mod_wsgi. 
That means that within Apache, these can’t be used together: 
you’ll have to switch out configurations, as shown below.

Ensure you have the Python development package, for the Python headers. 
And get the Apache development package:

    $ apt-get install apache2-dev


Download mod_wsgi from https://github.com/GrahamDumpleton/mod_wsgi/releases

Documentation for mod_wsgi is currently at https://code.google.com/p/modwsgi/ , 
but in the future will be at https://modwsgi.readthedocs.org/en/master/ .
There is an installation guide at https://code.google.com/p/modwsgi/wiki/QuickInstallationGuide

Configure mod_wsgi with Apache’s apxs, and for Python 3:

cd into the directory when extracting the mod_wsgi source. Configure and build mod_wsgi:

    $ ./configure —with-python=/usr/bin/python3
    $ make

Note that only ‘make install’ will create the actual mod_wsgi.so, 
but it will also try to install the file into its default place. 
We don’t want that, because we want to rename this mod_wsgi.so file 
(the --prefix option appears not to work).

    $ /usr/bin/apxs2 -i -S LIBEXECDIR=`pwd` -n 'mod_wsgi’ src/server/mod_wsgi.la
    $ mv mod_wsgi.so mod_wsgi3.so

Now place this file in /usr/lib/apache2/modules/.

Copy the wsgi loading files:

    $ cp /etc/apache2/mods-available/wsgi.load /etc/apache2/mods-available/wsgi3.load
    $ cp /etc/apache2/mods-available/wsgi.conf /etc/apache2/mods-available/wsgi3.conf

Update the wsgi3.load file to point to the mod_wsgi3.so file.
The wsgi3.conf can remain the same.
It simply has a lot of wsgi configuration options (commented out), 
that should be the same, irrelevant of the wsgi/Python version.

Link to the new wsgi.* files in /etc/apache2/mods-enabled/

Now create a new configuration file in /etc/apache2/sites-available, 
where the wsgi.load file is replaced by the wsgi3.load. 
Set WSGIPythonHome to /usr/bin/python3 
Note that this directive has to go outside any virtualhost.

Now it should be relatively easy to swap between mod_wsgi for 
Python 2 (the default) and mod_wsgi for Python 3. 
Note that you can’t run them next to each other, since the directives keywords
are the same (and are not always constrained to within a virtualhost).

We have made two scripts to easily switch between wsgi and wsgi3.

setup-apiweb2:
sudo a2dismod wsgi3
sudo a2enmod  wsgi 
sudo cp /etc/apache2/sites-available/www.astro.uva.nl-wsgi2.conf 
        /etc/apache2/sites-available/www.astro.uva.nl.conf
sudo service apache2 restart

setup-apiweb3:
sudo a2dismod wsgi
sudo a2enmod  wsgi3
sudo cp /etc/apache2/sites-available/www.astro.uva.nl-wsgi3.conf 
        /etc/apache2/sites-available/www.astro.uva.nl.conf
sudo service apache2 restart


--------------------------------------------------------------------------------------------

=== Update the local settings ===

Now, in the apiweb/settings directory, copy the local_template.py to local.py:

  $ cp apiweb/settings/local_template.py apiweb/settings/local.py


Update local.py with the necessary settings. Use a current settings file to fill out the details.


=== Copy and migrate the old databases ===

From within the root directory Create an ‘apiweb/databases’ subdirectory:

  $ mkdir -p apiweb/databases
  $ mkdir -p apiweb/databases/flickr

  $ setfacl -m u::rwx,u:www-data:rwx,g::rwx,o:rx apiweb/databases
  $ setfacl -m u::rwx,u:www-data:rwx,g::rwx,o:rx apiweb/databases/flickr


Now copy the old databases to the new website: 
Note the name change in the databases (api.db -> apiweb.db, ditto for api-wiki -> apiweb-wiki.db). 
For example:

  $ cp ~astroweb/apiweb/api/api/databases/api.db       apiweb/databases/apiweb.db
  $ cp ~astroweb/apiweb/api/api/databases/api-wiki.db  apiweb/databases/apiweb-wiki.db
 
  $ /usr/bin/setfacl -m u::rw,u:www-data:rw,g::rw,o::r apiweb/databases/apiweb.db
  $ /usr/bin/setfacl -m u::rw,u:www-data:rw,g::rw,o::r apiweb/databases/apiweb-wiki.db


Now migrate the current database to the latest version:

  $ python3 ./manage.py migrate

Migrating the databases means bringing them up to date with the current models. 
Django keeps changes to models in so-called migrations files, 
and that way, the database tables can easily be modified.

If you get an error when running the migration, 
the database is probably from before migrations (i.e., from an old project). 
Use the --fake-initial flag to circumvent the initial (0001) step of the migrations 
and avoid the error.

  $ python3 ./manage.py migrate --fake-initial

‘--fake-initial’ should only be used the first time. 
After that, the database is up to date, and can be migrated with just the ‘migrate’ command.

*Do not use the out-of-fashion JSON files dumps: this will confuse the database. 
Use the database “an sich”, and work from there
(i.e., don’t empty the database first, migrate, then fill it; just migrate the full database).

-------------------------------------------------------------------------------------------------

Now copy the pdf files of the phd theses to the staticfiles directory.

  cd apiweb/apps/research/static/research/
  cp -rf /home/astroweb/apiweb/api/api/apps/research/static/research/theses .


# Copy the uploaded media files:

  $ cd /home/martin/Websites/apiweb3/apiweb/media/
  $ mkdir  uploads
  $ mkdir _versions
  $ setfacl -d -m u::rwx,u:www-data:rwx,g::rwx,o:rx uploads
  $ setfacl -m    u::rwx,u:www-data:rwx,g::rwx,o:rx uploads
  $ setfacl -d -m u::rwx,u:www-data:rwx,g::rwx,o:rx _versions
  $ setfacl -m    u::rwx,u:www-data:rwx,g::rwx,o:rx _versions

  $ tar zxvf uploads.tar.gz

# Make versions and thumbnails of upload media for filebrowser:

  $ python3 ./manage.py fb_version_generate


Now migrate the general static directory

  $ python3 ./manage.py collectstatic

-----------------------------------------------------------------------------

Change apiweb/apps/urls.py:

  from filebrowser.sites import site

  urlpatterns = patterns[
     url(r'^admin/filebrowser/', include(site.urls)),
     url(r'^admin/', include(admin.site.urls)),
  ]

  
