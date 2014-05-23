import logging

from tastypie.authorization import DjangoAuthorization
from tastypie.http import HttpGone, HttpForbidden, HttpNoContent, HttpMultipleChoices, HttpApplicationError, HttpNotImplemented
from guardian.shortcuts import get_objects_for_user

logger = logging.getLogger(__name__)


class GuardianAuthorization(DjangoAuthorization):
    """

    GuardianAuthorization

        Object level permission checking with django-guardian for django models exposed via tastypie.

    :create_permission_code:
        the permission code that signifies the user can create one of these objects
    :view_permission_code:
        the permission code that signifies the user can view the detail
    :update_permission_code:
        the permission code that signifies the user can update one of these objects
    :remove_permission_code:
        the permission code that signifies the user can remove one of these objects

    :kwargs:
        other permission codes

    :return values:
        Empty list : When user requests a list of resources for which they have no
                     permissions for any of the items
        HttpForbidden : When user does not have nessecary permissions for an item
        HttpApplicationError : When resource being requested isn't a valid django model.



        class Something(models.Model):
            name = models.CharField()

        class SomethingResource(ModelResource):
            class Meta:
                queryset = Something.objects.all()
                authorization = GuardianAuthorization(
                    view_permission_code = 'can_view',
                    create_permission_code = 'can_create',
                    update_permission_code = 'can_update',
                    delete_permission_code = 'can_delete'
                    )

    """

    def __init__(self, *args, **kwargs):
        self.view_permission_code = kwargs.pop("view_permission_code", 'can_view')
        self.create_permission_code = kwargs.pop("create_permission_code", 'can_create')
        self.update_permission_code = kwargs.pop("update_permission_code", 'can_update')
        self.delete_permission_code = kwargs.pop("delete_permission_code", 'can_delete')
        super(GuardianAuthorization, self).__init__(*args, **kwargs)

    def generic_base_check(self, object_list, bundle):
        """
            Raises a HttpApplicationError exception if either:
                a) if the `object_list.model` doesn't have a `_meta` attribute
                b) the `bundle.request` object doesn have a `user` attribute
        """
        if not self.base_checks(bundle.request, object_list.model):
            raise HttpApplicationError("Invalid resource.")
        return True

    def generic_item_check(self, object_list, bundle, permission):
        """
            Single item check, returns boolean indicating that the user
            can access the item resource.
        """
        self.generic_base_check(object_list, bundle)
        if not bundle.request.user.has_perm(permission, bundle.obj):
            raise HttpForbidden("You are not allowed to access that resource.")

        return True

    def generic_list_check(self, object_list, bundle, permission):
        """
            Multiple item check, returns queryset of resource items the user 
            can access.

            TODO: debating whether to return an empty list or HttpNoContent
        """
        self.generic_base_check(object_list, bundle)
        return get_objects_for_user(bundle.request.user, permission, object_list)

    # List Checks
    def create_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.create_permission_code)

    def read_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.view_permission_code)

    def update_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.update_permission_code)

    def delete_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.delete_permission_code)

    # Item Checks
    def create_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.create_permission_code)

    def read_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.view_permission_code)

    def update_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.update_permission_code)

    def delete_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.delete_permission_code)
