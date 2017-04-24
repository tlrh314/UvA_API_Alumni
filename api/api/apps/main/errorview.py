from django.conf import settings
from django.template import loader
from django.http import HttpResponseServerError
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def server_error(request, template_name='500.html'):
    """Make sure STATIC_URL is included in the 500 page
    From http://www.djangosnippets.org/snippets/1199/"""

    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(context={'STATIC_URL': settings.STATIC_URL}))
