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
from django.db.models.base import ObjectDoesNotExist
from slugify import slugify


LOGGER = logging.getLogger(__name__)

I4P_PATH = os.getenv('I4P_PROJECT_SOURCE_PATH',
                     os.path.expanduser('~/sources/imaginationforpeople'))

API_URL = os.getenv('IP2IS_DESTINATION_URL',
                     'http://data.patapouf.org/api/v0')
                     # 'http://127.0.0.1:8002/api/v0')
API_USERNAME = os.getenv('IP2IS_API_USERNAME', 'admin')
API_PASSWORD = os.getenv('IP2IS_API_PASSWORD', 'Xdelfino06') # patapouf
#API_PASSWORD = os.getenv('IP2IS_API_PASSWORD', 'admin')
API_KEY = os.getenv('IP2IS_API_KEY', '9ea94d6723509fd21fc1518e00c541743e33b154') # patapouf
#API_KEY = os.getenv('IP2IS_API_KEY', '93a932dd3037378d11a50ba583009a30c0dc8603')

if API_PASSWORD:
    LOGGER.warning(u'Using API_USERNAME %s.', API_USERNAME)
    api = slumber.API(API_URL, auth=(API_USERNAME, API_PASSWORD))

elif API_KEY:
    LOGGER.warning(u'Using API_KEY %s.', API_KEY)
    api = slumber.API(API_URL, api_key=API_KEY)

else:
    LOGGER.warning(u'Connecting anonymously.')
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
    #LOGGER.warning('Getting object id for = %s', obj)

    try:
        try:
            return obj['objects'][0]['id']

        except KeyError:
            #LOGGER.warning('OBJECT_ID id = %s', obj['id'])
            return obj['id']

    except:
        #LOGGER.warning('DID NOT FOUND ID for obj: %s', obj)
        return None


def api_get(api_object_path, natural_key, **kwargs):
    """ Get an object on the remote API, pivoting on natural_key. """

    # LOGGER.warning('API get : %s %s %s',
    #                api_object_path, natural_key,
    #                kwargs)

    obj = api_object_path.get(**natural_key)

    # LOGGER.warning('GET: %s', obj)

    if has_result(obj):
        return object_id(obj)

    else:
        return None

def api_create_only(api_object_path, natural_key, **kwargs):
    """ create an object on the remote API, pivoting on natural_key. """

    # LOGGER.warning('API create ONLY: %s %s %s',
    #                api_object_path, natural_key,
    #                kwargs)

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

    raise RuntimeError('Could not create {} on {} with {}'.format(
                       natural_key, api_object_path, kwargs))



def api_get_or_create(api_object_path, natural_key, no_update=None, **kwargs):
    """ Get or create an object on the remote API, pivoting on natural_key. """

    # LOGGER.warning('API get or create: %s %s %s',
    #                api_object_path, natural_key,
    #                kwargs)

    obj = api_object_path.get(**natural_key)

    # LOGGER.warning('GET: %s', obj)

    if has_result(obj):
        return object_id(obj)

    else:
        #LOGGER.warning('## POsting (before): %s', kwargs)
        #LOGGER.warning('>>>>> Update ?: %s', no_update)
        if not no_update:
            kwargs.update(natural_key)
        #R.warning('## POsting (after): %s', kwargs)

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

    LOGGER.warning('postal address = %s', postal_address)
    # FIXME : ugly solution, but problem is Tastypie does not by default does not accept
    # to create an object that contains another one (here PostalAddress) with id only
    # we have to give resource_uri BUT fecthing a Place object by filtering resource_uri does not work
    # hence the splitting in 2 steps: 1) check existence with mere id 2) create by giving ressource_uri
    if postal_address:
        place = api_get(
            api.scout.place,
            {'address': postal_address}
            )
        if place:
            return place
        else:
            return api_create_only(
            # return object_id(api_get_or_create(
                api.scout.place,
                {'address': ('api/v0/scout/postaladdress/%s' % (postal_address))},
                # {'address': object_id(postal_address)}
            )

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
        try:
            obj_id = object_id(api.project.progress.get(range__name=progress_range_name))
            if obj_id:
                PROGRESS[progress_range_name] = api_get_or_create(
                    api.project.progress,
                    {'id':obj_id},
                )
                pass
            else:
                PROGRESS[progress_range_name] = api_create_only(
                    api.project.progress,
                    {'range':{'name': progress_range_name}, "label":progress_range_name},
                )

        except:
            LOGGER.warning("error getting progress")
            pass
    progress_string = str(PROGRESS)
    LOGGER.warning('Finished populate Progress %s', progress_string)

def populate_questions():
    """ populate questions to migrate projects & references. """

    # They are required to import I4P projects.
    # NOTE: weight/order is to be migrated by hand.

    TEMPLATES_SLUGS = ('ip', 'is', 'generic', )

    for template_slug in TEMPLATES_SLUGS:
        TEMPLATES[template_slug] = api_get_or_create(
            api.project.sheet.template,
            {'slug': template_slug},
            name=template_slug,
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

    LOGGER.warning('Finished populate question %s', QUESTIONS)

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
            LOGGER.warning(' migrating project %s', (project.pk))
            if pivot_project is None:
                pivot_project = project.id

            try:
                if project.master.locations.all().count() > 0:
                    place_id = place_from_location(
                        project.master.locations.all().order_by('id')[0])
                    if place_id != None:
                        location = ('api/v0/scout/place/%s' % (place_id))
                    else:
                        location = None

                else:
                    location = None

                LOGGER.warning('title ? = %s, str(%s)', project.title, project.title)
                if project.master.status:
                    progress_value = PROGRESS[project.master.status]
                else:
                    progress_value = None
                project_id = api_get_or_create(
                    api.project.project,
                    {'slug': project.slug,
                     'language_code' : project.language_code,
                    },
                    no_update=True,
                    slug=project.slug+'_'+project.language_code,
                    language_code=project.language_code,
                    data={
                        'topics': [
                            u'{0}: {1}'.format(t.site.name, t.topic)
                            for t in project.master.topics.all()
                        ],
                    },
                    location=location,
                    title=project.title,
                    baseline=project.baseline,
                    created_on=project.master.created.isoformat(),
                    description=project.about_section,
                    progress=('api/v0/project/progress/%s' % (progress_value)),
                    transient_project_original_id=pivot_project,
                    website=project.master.website,
                    groups=[GROUPS[s.name] for s in project.master.site.all()],
                )

                for tag in [x.strip() for x in project.themes.split(',')]:
                    # FIXME : tags "déforestation" and "deforestation" get the same slug
                    # so we should check before that no other tag with same slug do not already exist
                    taggeditem_tag = api_get(
                        api.taggeditem,
                        {'object_type_name':'project',
                        'object_id':project_id,
                        'tag__name':tag}
                    )
                    LOGGER.warning(' [TAG] Tagging (for %s)already there %s', tag, taggeditem_tag)
                    if not taggeditem_tag:
                        # check if tag object with same slug exists
                        tag_object = api.tag.get(slug=slugify(tag))
                        LOGGER.warning(' [TAG] Tag object %s equal to %s', tag_object, tag)
                        try:
                            api_create_only(
                                api.taggeditem.project(project.id),
                                {'tag':tag_object['objects'][0]['name']}
                            )
                        except:
                            api_create_only(
                                api.taggeditem.project(project.id),
                                {'tag':tag}
                            )

                if project_id != None:
                    LOGGER.warning(' PROJECT ID = %s', project_id)
                    project_sheet_id = api_get_or_create(
                        api.project.sheet.projectsheet,
                        {'project':project_id},
                        project=('api/v0/project/project/%s' % (project_id)),
                        template=('/api/v0/project/sheet/template/%s' % (TEMPLATES['is'],)),
                        no_update=True
                        )
                else:
                    LOGGER.warning(' NO PROJECT ID !!')
                    pass

                # migrating project pictures
                pictures = project.master.pictures.all()
                LOGGER.warning(' />/>/>/>/>/>/ got pictures ? %s', (pictures))
                project_sheet = api.project.sheet.projectsheet(project_sheet_id)
                remote_files = project_sheet.get()['bucket']['files']
                files_length = len(project_sheet.get()['bucket']['files'])
                LOGGER.warning(' files_length = %s', files_length)
                remote_files_name = []
                for file in remote_files:
                    remote_files_name.append(file.filename)
                bucket_id = project_sheet.get()['bucket']['id']
                LOGGER.warning(' bucket for project sheet id %s ? %s', project_sheet_id, bucket_id)
                LOGGER.warning(' remote_files_name = %s', remote_files_name)
                for idx, pic in enumerate(pictures):
                    picture = pic._imgfield
                    with picture.file as fp:
                        try:

                            # check file does not already exist
                            local_filename = pic._imgfield.file.name.rsplit('/',2)[2]
                            LOGGER.warning(' FILES ::: local_filename = %s', local_filename)
                            if local_filename not in remote_files_name:
                                LOGGER.warning(' NO FILES YET')
                                post_url = API_URL.rsplit('/', 2)[0]+'/bucket/upload/'
                                headers = {'Authorization' : ('apikey %s:%s' % (API_USERNAME, API_KEY))}

                    i                       res = requests.post(
                                    post_url,
                                    headers=headers,
                                    data=[('bucket', bucket_id)],
                                    files={'file': fp}
                                )

                                LOGGER.warning('// POSTED FILE // : res = %s ', res)
                                if idx == 0:
                                    # set as cover picture if first in the list
                                    file_resource_uri = res.json()['resource_uri']

                                    project_sheet.patch({'cover': file_resource_uri})
                        except:
                            LOGGER.warning('/>/>/>/>/>/>/ Error posting picture n° %s', idx)
                            pass

                answers = []

                for answer in project.master.answers.all():
                    try:
                        # Answers have translations as well!! fixed by giving language code, else english is allways given
                        answer = answer.translations.all().filter(language_code=project.language_code)[0]
                        answers.append(
                            api_get_or_create(
                                api.project.sheet.question_answer,
                                {
                                    'question': QUESTIONS[answer.question_id],
                                    'projectsheet': project_sheet_id,
                                },
                                answer=answer.content,
                                question=('/api/v0/project/sheet/question/%s' % (QUESTIONS[answer.question_id])),
                                projectsheet=('api/v0/project/sheet/projectshn  eet/%s' % (project_sheet_id)),
                                no_update=True,
                            )
                        )
                    except:
                        LOGGER.warning('no content for question %s', (answer.question_id))
                        pass
                # Add references as question-anwser
                api_get_or_create(
                    api.project.sheet.question_answer,
                    {
                        'question': QUESTIONS[99],
                        'projectsheet': project_sheet_id,
                    },
                    answer=u'\n'.join(
                        ref.desc
                        for ref in project.master.references.all()),
                    question=('/api/v0/project/sheet/question/%s' % (QUESTIONS[99])),
                    projectsheet=('api/v0/project/sheet/projectsheet/%s' % (project_sheet_id)),
                    no_update=True,
                )

                # TO me, for migrating users we need an official aggreement.

                # for member in project.master.members.values_list('username',
                #                                           flat=True):
                #     api.objectprofilelink.project(project_id).post({
                #         'detail': 'member',
                #         'level': 0,
                #         'profile_id': PROFILES[member],
                #         'isValidated':True
                #     })
                #
                # for fan in project.master.fans.values_list('username', flat=True):
                #     api.objectprofilelink.project(project_id).post({
                #         'detail': 'member',
                #         'level': 2,
                #         'profile_id': PROFILES[fan],
                #         'isValidated':True
                #     })
            except:
                LOGGER.exception('Could not migrate %s', project)

    LOGGER.info('migrated %s projects.', projects.count())


def migrate():
    """ Migrate everything. """

    OLD_PWD = os.getcwd()

    os.chdir(I4P_PATH)

    try:
        #migrate_users()
        migrate_groups()
        #migrate_profiles()
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
            logging.getLogger(module).setLevel(logging.INFO)

        migrate()
