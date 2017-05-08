# from django.contrib.auth.models import User
from django.db.models import Q

from ajax_select import register, LookupChannel

from ..alumni.models import Alumnus

@register('alumnus')
class AlumnusLookup(LookupChannel):

    model = Alumnus

    def get_query(self, q, request):
        multifilter = Q()
        for search_term in q.split():
            multifilter = (multifilter | Q(last_name__icontains=search_term)
                | Q(first_name__icontains=search_term))

        return self.model.objects.filter(multifilter).order_by('last_name')

    def format_item_display(self, item):
        return u"<span class='tag'>Selected Alumnus: {0}</span>".format(item.full_name)


# @register('author')
# class AuthorLookup(LookupChannel):
#
#     model = User
#
#     def get_query(self, q, request):
#         return self.model.objects.filter(last_name__icontains=q).order_by('last_name')
#
#     def format_item_display(self, item):
#         return u"<span class='tag'>%s</span>" % item.alumnus.last_name
