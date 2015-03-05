Unisson Data Server
===================

A RESTfull API server for various needs and a framework for developing distributed Commons services.

A sandbox where we experiment with [Commons](http://wealthofthecommons.org/about)[EN] through REST APIs.

This server is inspired by the [Unisson Method](http://unisson.co/fr/projectbc/)[FR].

API list:

- Bucket (beta) : File manager
- Flipflop (beta) : Kanban boards
- Scout (beta) : Map
- Transport/Vlille (beta) : Lille Public Bike Service
- Alambic (pre-alpha) : Room discussion- Projects : anything that can be qualified as a Project
- Graffiti: Tags (from `taggit`) & Django content types ressources
- ProjectSheet : Project Description
- Commons : Determine wich "commons project" to use for a given usage
- Unisson : Evaluate "commons project" with the Unisson method


Authors / contributors:
  - Guillaume Libersat
  - Simon Sarrazin
  - Alban Tiberghen
  - Freddy Limpens
  - Olivier Cortès

See COPYING for license.



# Roadmap

Our next step is to decouple the APIs by using a standard such as [Json Linked Data](http://json-ld.org/).



# How to install ?

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



## Getting the code
 
Once you're in your virtualenv directory, use::

    git clone https://github.com/UnissonCo/dataserver/
    cd dataserver
  
fetch the dependencies using::

    pip install -r requirements.txt
  
*It may be the right time to fetch a cup of coffee! :-)*

.. note::

  From now on, the ``dataserver`` directory will be called **the project root** (or **PROJECT_ROOT**).



## Configuring the database / cache

You have the choice to install a Postgis or Sqlite database. Sqlite is easier to get a test environment.

You should have redis running on 127.0.0.1 for automatic configuration. Else, define the environment variable `DATASERVER_REDIS_CACHE_DB`. The default value is `'127.0.0.1:6379:2'`. Please always specify the *port*, even if it's the default one (6379).


### PostGis DB

If you use a postgresql backend, you need to install postgis (`sudo apt-get install postgis` on Debian / Ubuntu).

You need to generate the postgis template before syncing your database. As `postgres` user, create a `template_postgis` template database then the data server DB:

    sudo -i -u postgres
    createdb -E UTF8 template_postgis
    
    # Tune this to your version's setup 
    POSTGIS_PATH="/usr/share/postgresql/contrib/postgis-2.1"
    
    psql -d template_postgis -f ${POSTGIS_PATH}/postgis.sql
    psql -d template_postgis -f ${POSTGIS_PATH}/spatial_ref_sys.sql
    
    cat << EOF | psql -d template_postgis
    GRANT ALL ON geometry_columns TO PUBLIC;
    GRANT ALL ON spatial_ref_sys TO PUBLIC;
    GRANT ALL ON geography_columns TO PUBLIC;
    EOF
    
    createuser dataserver -P
    createdb -E utf8 -O dataserver dataserver -T template_postgis

Also don't forget to edit your `/etc/postgresql/*/main/pg_hba.conf` file if you are starting from a fresh postgres installation:

    local   all             all       md5

then:

    sudo service postgresql restart
  
  
  
###  SQlite
 
Install spatialite:

    sudo apt-get install libspatialite5

Change settings.py:

    'ENGINE': 'django.contrib.gis.db.backends.spatialite',
    'NAME': 'dataserver.db',



### (Optional) Elastic Search

The `bucket` module requires elastic search. If you plan to use it, you should install `ES` and configure it (alongside `haystack`) in `site_settings` (see below). 



### Tune your Django settings

Use the `site_settings` template for your own settings:

    cp dataserver/site_settings.py.tmpl dataserver/site_settings.py

You can tune the database configuration URL with the `UNISSON_DATA_SERVER_DATABASE` environment variable (this follows the [12factor recommendations](http://12factor.net/config)). Default value doesn't need any tuning if you set `dataserver` as the database user/password/name.



### Populating the Database & starting the data-server

Then you need to initialize your database with these commands:

    python manage.py syncdb
    python manage.py migrate --all
    python manage.py check_permissions

Django will prompt for a user creation, this is always a good idea to say *yes*:

     You just installed Django's auth system, which means you don't have any superusers defined.
     Would you like to create one now? (yes/no): y

Now, run the server:

    python manage.py runserver



## Licenses

This software is licensed under the AGPLv3 (See COPYING file for more information).

The media (pictures, sounds, videos, ...) are licensed under the Creative Commons CC-BY-SA (See MEDIA_COPYING for more information).
