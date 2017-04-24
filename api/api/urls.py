import sys

from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

handler500 = 'api.apps.main.errorview.server_error'

# Normal URLs
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('api.apps.blog.urls')),
    url(r'^institute/', include('api.apps.institute.urls', namespace='institute')),
    url(r'^people/', include('api.apps.people.urls', namespace='people')),
    url(r'^', include('api.apps.alumni.urls')),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

