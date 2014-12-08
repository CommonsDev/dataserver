from tastypie.authentication import ApiKeyAuthentication

class AnonymousApiKeyAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        # Run the super method, but don't return what we get back.
        # This will populate ``request.user`` is they're auth'd.
        result = super(AnonymousApiKeyAuthentication, self).is_authenticated(request, **kwargs)

        if result is True or request.method == 'GET':
            return True

        return self._unauthorized()
