# -*- coding: utf-8 -*-
""" Migration I4P → IS.

Usage:

    # In one console:
    cd ~/sources
    git clone https://github.com/CommonsDev/dataserver
    cd dataserver
    # create a virtualenv, populate it, make the dataserver run…
    ./manage.py runserver 0.0.0.0:8002

    # In another
    cd ~/sources
    git clone https://github.com/ImaginationForPeople/imaginationforpeople
    cd imaginationforpeople
    # create a virtualenv, populate it, make the django
    # project run, and clone the i4p database locally.
    cd apps/i4p_base/management/commands
    ln -sf ~/sources/dataserver/contrib/ip2is.py
    ./manage.py ip2is

"""

from __future__ import unicode_literals

import os
import slumber
import logging
import requests

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

LOGGER = logging.getLogger(__name__)

I4P_PATH = os.getenv('I4P_PROJECT_SOURCE_PATH',
                     os.path.expanduser('~/sources/imaginationforpeople'))

API_URL = os.getenv('IP2IS_DESTINATION_URL',
                    # 'http://data.patapouf.org/api/v0')
                    'http://127.0.0.1:8002/api/v0')
API_USERNAME = os.getenv('IP2IS_API_USERNAME', 'admin')
API_PASSWORD = os.getenv('IP2IS_API_PASSWORD', 'admin')
API_KEY = os.getenv('IP2IS_API_KEY', None)
# '5d0eccabb50b76c08d83f112f9f003f2b50b629a'

if API_PASSWORD:
    LOGGER.info(u'Using API_USERNAME %s.', API_USERNAME)
    api = slumber.API(API_URL, auth=(API_USERNAME, API_PASSWORD))

elif API_KEY:
    LOGGER.info(u'Using API_KEY %s.', API_KEY)
    api = slumber.API(API_URL, api_key=API_KEY)

else:
    LOGGER.info(u'Connecting anonymously.')
    api = slumber.API(API_URL)

# get all projecs. JSON translated to res.attrs
# projects = api.project.project.get()['objects']
#
# get a project. JSON in res.attrs
# project = api.project.project(21).get()

PROGRESS_RANGES = (
    'IDEA',
    'BEGIN',
    'WIP',
    'END',
)


# ——————————————————————————————————————————————————————————————————— Migration

def has_result(obj):
    """ Wrap the slumber/tastypie API result to know if we got something. """

    return obj['meta']['total_count'] > 0


def object_id(obj):
    """ Wrap the slumber/tastypie API result to get the object ID. """

    try:
        try:
            return obj['objects'][0]['id']

        except KeyError:
                return obj['id']

    except:
        LOGGER.warning('obj: %s', obj)
        raise


def api_get_or_create(api_object_path, natural_key, **kwargs):
    """ Get or create an object on the remote API, pivoting on natural_key. """

    # LOGGER.debug('API get or create: %s %s %s',
    #                api_object_path, natural_key,
    #                kwargs)

    obj = api_object_path.get(**natural_key)

    # LOGGER.warning('GET: %s', obj)

    if has_result(obj):
        return object_id(obj)

    else:
        kwargs.update(natural_key)

        res = api_object_path.post(data=kwargs)

        if res:
            return object_id(res)

        try:
            return kwargs['id']

        except:
            obj = api_object_path.get(**natural_key)

            if has_result(obj):
                return object_id(obj)

        raise RuntimeError('Could not get or create {} on {} with {}'.format(
                           natural_key, api_object_path, kwargs))

USERS = {}
GROUPS = {}
PROFILES = {}
TEMPLATES = {}
QUESTIONS = {}
PROGRESS = {}


def place_from_location(location_object):
    """ Get the scout place (geomapping) from postal address. """

    postal_address = None

    if location_object.address:
        if location_object.country:
            postal_address = api_get_or_create(
                api.scout.postaladdress,
                {
                    'street_address': location_object.address,
                    'country': location_object.country.code,
                },
            )

        else:
            postal_address = api_get_or_create(
                api.scout.postaladdress,
                {'street_address': location_object.address},
            )

    elif location_object.country:
        postal_address = api_get_or_create(
            api.scout.postaladdress,
            {'country': location_object.country.code},
        )

    if postal_address:
        return object_id(api_get_or_create(
            api.scout.place,
            {'address': object_id(postal_address)}
        ))

    return None


def migrate_users():
    """ migrate users. """
    # http://localhost:8002/api/v0/account/user/schema

    from userena.models import get_user_model
    User = get_user_model()

    # Avoid the AnonymousUser, it fails to be added via the API.
    users = User.objects.filter(id__gte=1)
    errors = []

    LOGGER.info('migrating users…')

    for user in users:
        try:
            USERS[user.username] = api_get_or_create(
                api.account.user,
                {'username': user.username[:30]},
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )

        except:
            LOGGER.exception('Could not migrate %s', user)
            errors.append(user)

        # TODO: PASSWORDS !!

    LOGGER.info('migrated %s users (%s errors).', users.count(), len(errors))


def migrate_groups():
    """ migrate groups. """
    # http://localhost:8002/api/v0/account/group/schema

    LOGGER.info('migrating sites to groups…')

    sites = Site.objects.all()
    errors = []

    for site in sites:
        try:
            GROUPS[site.name] = api_get_or_create(
                api.account.group,
                {'name': site.name},
            )

        except:
            LOGGER.exception('Could not migrate %s', site)
            errors.append(site)

    LOGGER.info('migrated %s sites (%s error(s)).', sites.count(), len(errors))


def migrate_profiles():
    """ migrate profiles. """
    # http://localhost:8002/api/v0/account/profile/schema

    from imaginationforpeople.apps.member.models import I4pProfile

    LOGGER.info('migrating profiles…')

    profiles = I4pProfile.objects.all()
    errors = []

    for profile in profiles:
        try:
            kwargs = dict(
                website=profile.website,
                description=profile.about,
                privacy=profile.privacy,
                language=profile.language,
                data={
                    'registration_site': profile.registration_site.name,
                    'gender': profile.gender,
                    'birthday': profile.birthday,
                },
            )

            place_id = place_from_location(profile)

            if place_id is not None:
                kwargs['place'] = place_id

            PROFILES[profile.user.username] = api_get_or_create(
                api.account.profile,
                {'user': USERS[profile.user.username]},
                **kwargs
            )

        except:
            LOGGER.exception('Could not migrate %s', profile)
            errors.append(profile)

    LOGGER.info('migrated %s profiles (%s errors).',
                profiles.count(), len(errors))


def populate_progress_ranges():
    """ populate progress ranges to migrate projects. """

    # They are required to import I4P projects.
    # NOTE: weight/order is to be migrated by hand.

    for progress_range_name in PROGRESS_RANGES:
        PROGRESS[progress_range_name] = api_get_or_create(
            api.project.progress.range,
            {'slug': progress_range_name},
        )


def populate_questions():
    """ populate questions to migrate projects & references. """

    # They are required to import I4P projects.
    # NOTE: weight/order is to be migrated by hand.

    TEMPLATES_SLUGS = ('ip', 'is', 'generic', )

    for template_slug in TEMPLATES_SLUGS:
        TEMPLATES[template_slug] = api_get_or_create(
            api.project.sheet.template,
            {'slug': template_slug},
        )

    QUESTIONS_SLUGS = (
        ('is', 'innovation', 1, ),
        ('is', 'social', 4, ),
        ('is', 'potentiel', 3, ),
        ('is', 'creation', 5, ),
        ('is', 'business-model', 2, ),
        ('is', 'collectif', 45, ),
        ('is', 'environnement', 46, ),
        ('generic', 'references', 99, ),
    )

    for template_slug, question_slug, i4p_id in QUESTIONS_SLUGS:
        QUESTIONS[i4p_id] = api_get_or_create(
            api.project.sheet.question,
            {'slug': question_slug},
            template_id=TEMPLATES[template_slug]
        )


def migrate_projects():
    """ Migrate projects. """

    from imaginationforpeople.apps.project_sheet.models import I4pProject

    # In [90]: I4pProject.objects.language('fr').filter(topics=1).count()
    # Out[90]: 1774
    #
    # In [91]: I4pProject.objects.language('en').filter(topics=1).count()
    # Out[91]: 1296

    projects = I4pProject.objects.filter(topics=1)

    LOGGER.info('migrating projects…')

    for project_untranslated in projects:
        pivot_project = None
        for project in project_untranslated.translations.all():
            if pivot_project is None:
                pivot_project = project.id

            try:
                place_id = place_from_location(
                    project.locations.all().order_by('id')[0])

                project_id = api_get_or_create(
                    api.project.project,
                    {'slug': project.slug},
                    # …
                    data={
                        'topics': [
                            u'{0}: {1}'.format(t.site.name, t.topic)
                            for t in project.topics.all()
                        ],

                    },
                    location=place_id,
                    title=project.title,
                    baseline=project.baseline,
                    created_on=project.created,
                    description=project.about_section,
                    progress={'range': PROGRESS[project.completion_progress]},
                    language_code=project.language_code,
                    transient_project_original_id=pivot_project,
                    website=project.website,
                    groups=[GROUPS[s.name] for s in project.site.all()],
                )

                for tag in [x.strip() for x in project.themes.split(',')]:
                    api_get_or_create(
                        api.taggeditem.project(project.id),
                        tag=tag.name
                    )

                project_sheet_id = api_get_or_create(
                    project=project_id,
                    template=TEMPLATES['is'],
                )

                picture = project.cover_picture._imgfield

                with picture.open() as fp:

                    project_sheet = api.project.sheet(project_sheet_id)

                    res = requests.post(
                        API_URL.rsplit('/', 2)[0],
                        data={
                            'bucket': project_sheet.get()['bucket']['id']
                        },
                        files={
                            'file': fp
                        }
                    )

                    file_resource_uri = res.json()['resource_uri']

                    project_sheet.patch({'cover': file_resource_uri})

                for member in project.members.values_list('username',
                                                          flat=True):
                    api.objectprofilelink.project(project_id).post({
                        'detail': 'member',
                        'level': 0,
                        'profile_id': PROFILES[member.username]
                    })

                for fan in project.fans.values_list('username', flat=True):
                    api.objectprofilelink.project(project_id).post({
                        'detail': 'member',
                        'level': 2,
                        'profile_id': PROFILES[member.username]
                    })

                answers = []

                for answer in projects.answers.all():
                    answers.append(
                        api_get_or_create(
                            api.project.sheet.question_answer,
                            {
                                'question': QUESTIONS[answer.id],
                                'projectsheet': project_sheet_id,
                            },
                            answer=answer.content,
                        )
                    )

                api_get_or_create(
                    api.project.sheet.question_answer,
                    {
                        'question': QUESTIONS[99],
                        'projectsheet': project_sheet_id,
                    },
                    answer=u'\n'.join(
                        ref.desc
                        for ref in project.references.all()),
                )

            except:
                LOGGER.exception('Could not migrate %s', project)

    LOGGER.info('migrated %s projects.', projects.count())


def migrate():
    """ Migrate everything. """

    OLD_PWD = os.getcwd()

    os.chdir(I4P_PATH)

    try:
        migrate_users()
        migrate_groups()
        migrate_profiles()
        populate_progress_ranges()
        populate_questions()
        migrate_projects()

    finally:
        os.chdir(OLD_PWD)


class Command(BaseCommand):

    """ Migrate I4P to IS. """

    help = 'Migrate I4P to IS.'

    def handle(self, *args, **options):
        """ Unleash the kraken. """
        for module in (
            'requests',
            'django',
            'keyedcache',
        ):
            logging.getLogger(module).setLevel(logging.CRITICAL)

        migrate()
