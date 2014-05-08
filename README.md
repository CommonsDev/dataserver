Unisson Data Server
===================

A collection of REST APIs that provides various services. 

You need to patch tastypie using this:
https://github.com/toastdriven/django-tastypie/pull/930

Author: Guillaume Libersat. See COPYING for license.

# REQUIREMENTS #
## PostGis DB ##
You need to hook up this dataserver to a postgis enabled DB. Below are instructions when 
using postgreSQL.   

First, just run as "postgres" user the [following script](https://github.com/JoshData/boundaries_us/blob/master/misc/create_template_postgis-debian.sh)
This will create a template named `template_postgis` to use when creating the DB. You can now create a "gup" user and 
create the DB with the following code:

  $ createdb -U gup -E utf8 -O gup gup -T template_postgis
  
Then, usual `manage.py syncdb` and `manage.py migrate --all` will do the rest.
