from tastypie.authentication import ApiKeyAuthentication

class AnonymousApiKeyAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        # Run the super method, but don't return what we get back.
        # This will populate ``request.user`` is they're auth'd.
        result = super(AnonymousApiKeyAuthentication, self).is_authenticated(request, **kwargs)

        if result is True:
            return True

        if request.user.is_anonymous():
            # They're not auth'd. If it's a GET, let them through.
            # Otherwise, deny.
            if request.method != 'GET':
                print "No GET"                
                return self._unauthorized()
            else:
                print "Anonymous"
                return True

        return self._unauthorized()
