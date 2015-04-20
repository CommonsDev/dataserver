# -*- encoding: utf-8 -*-
import csv
from optparse import make_option
from geopy import geocoders

from django.core.management.base import BaseCommand, CommandError

from commons.models import Usage, Pertinence
from projects.models import Project
from scout.models import PostalAddress, Place
from unisson.models import EvaluationIngredient, Ingredient

class Command(BaseCommand):
    help = 'Import projects from a CSV file'

    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest = "filename",
            help = "specify import file",
            metavar = "FILE"
        ),
    )


    def handle(self, *args, **options):
        filepath = options['filename']

        geolocator = geocoders.GoogleV3(domain='maps.google.fr', api_key='AIzaSyDQaSjOGFvA53s2vcOssz2SOnApxIH5kfI')

        import codecs

        try:
            with open(filepath, 'r') as csvfile:
                csv_file = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in csv_file:
                    title = row[0].decode('utf-8')
                    locality = row[1].decode('utf-8')
                    category = row[4].decode('utf-8')
                    proj_type = row[6].decode('utf-8')

                    pa, created = PostalAddress.objects.get_or_create(country=u"FR", address_locality=locality.lower(), postal_code=int(row[2]))
                    lookaddr = u"%s %s %s" % (pa.postal_code, pa.address_locality, pa.country)
                    print lookaddr
                    location = geolocator.geocode(lookaddr, exactly_one=True)
                    # import time
                    #time.sleep(2)
                    print unicode(location)
                    from django.contrib.gis.geos import Point
                    print location.latitude
                    place, created = Place.objects.get_or_create(address=pa, geo=Point(location.longitude, location.latitude))

                    from django.utils.text import slugify
                    project, created = Project.objects.get_or_create(title=title, slug=slugify(title), location=place, baseline=proj_type)

                    project.tags.add(category)
                    project.tags.add(proj_type)

                    project.save()

                    EvaluationIngredient.objects.get_or_create(ingredient=Ingredient.objects.get(ingredient="juridique"), project=project, adoption=EvaluationIngredient.ADOPTION_CHOICES[3][0], comment=unicode(row[7]))

                    usage, created = Usage.objects.get_or_create(label=proj_type)
                    Pertinence.objects.get_or_create(usage=usage, project=project)
                    print '.'
            # Ouvrir fichier CSV
            # Créer projet
            # Créer localité
            # Créer ingrédient juridique
            # poll = Poll.objects.get(pk=poll_id)
            pass
        except Exception, e:
            raise CommandError('Error while parsing "%s" %s ' % (filepath, e))

        self.stdout.write('Successfully imported csv file "%s"' % filepath)
