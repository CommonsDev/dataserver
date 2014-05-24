Unisson Data Server
===================

A temporary space for experimenting with REST APIs.
In a near future, the data server will become a framework for developing distributed web services.
The is a technical companion to the [Unisson Method](http://unisson.co/fr/projectbc/)[FR].

Author: Guillaume Libersat. See COPYING for license.

API list :

- Bucket (beta) : File manager
- Flipflop (beta) : Kanban boards
- Scout (beta) : Map
- Transport/Vlille (beta) : Lille Public Bike Service
- Groupbuying (pre-alpha) : Grouped buying system
- Alambic (pre-alpha) : Room discussion


Roadmap
=======

Our next step is to decouple the APIs by using a standard such as [Json Linked Data](http://json-ld.org/).


How to install ?
================

First, you need to setup an isolated developement environment for the
python apps using *virtualenv*. If you don't have *virtualenv*, you can
install it using your package manager such as *apt* if you're on
debian:

    apt-get install python-virtualenv
    virtualenv dataserver-env

Then, enters the environment:

    cd dataserver-env
    source bin/activate
  
Your prompt should update to something like (note the prefix):

    (dataserver-env)glibersat@carpe:~/Source/dataserver-env
    
.. warning:: For all next steps, you need to be in an activated environment.
  
  
###Getting the code


Once you're in your virtualenv directory, use::

    git clone https://github.com/UnissonCo/dataserver/
    cd dataserver
  
fetch the dependencies using::

    pip install -r requirements.txt
  
*It may be the right time to fetch a cup of coffee! :-)*

.. note::

  From now on, the ``dataserver`` directory will be called **the project root** (or **PROJECT_ROOT**).


Database configuration
---

You have the choice to install a Postgis or Sqlite database. Sqlite is easier to get a test environment :

##### PostGis DB
If you use a postgresql backend, you need to install postgis ( `sudo apt-get install postgis` ).

You need to generate the postgis template before syncning your database :

First, just run as "postgres" user the [following script](https://github.com/JoshData/boundaries_us/blob/master/misc/create_template_postgis-debian.sh)
This will create a template named `template_postgis` to use when creating the DB. You can now create a "dataserver" user and 
create the DB with the following code:

  $ createdb -U gup -E utf8 -O dataserver dataserver -T template_postgis
  
  
#####  SQlite 
Install spatialite ( `sudo apt-get install libspatialite5` )

Change settings.py : 
  'ENGINE': 'django.contrib.gis.db.backends.spatialite', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
  'NAME': 'dataserver.db',                      # Or path to database file if using sqlite3.


### Populating the Database


Then you need to initialize your database with these commands::

    python manage.py syncdb 
    python manage.py migrate --all
    python manage.py check_permissions


Django will prompt for a user creation, this is always a good idea to say *yes*::

     You just installed Django's auth system, which means you don't have any superusers defined.
     Would you like to create one now? (yes/no): **yes**


Now, run the server::

    python manage.py runserver


Licenses
========

This software is licensed under the AGPLv3 (See COPYING file for more information).

The media (pictures, sounds, videos, ...) are licensed under the Creative Commons CC-BY-SA (See MEDIA_COPYING for more information).
