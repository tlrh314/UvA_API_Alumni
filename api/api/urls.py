from django.contrib import admin
from django.conf.urls import url, include

handler500 = 'api.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('api.apps.blog.urls')),
    url(r'^people/', include('api.apps.people.urls', namespace='people')),
    url(r'^', include('api.apps.alumni.urls')),

]

