from __future__ import unicode_literals, absolute_import, division

from django.views.generic import DetailView
from ..news.views import DateOrderedListView
from .models import Job


class JobsView(DateOrderedListView):
    template_name = 'jobs/job_list.html'
    date_key = 'deadline'
    order_keys = ('deadline',)
    limit_by_date_onoff = True
    model = Job

class JobDetailView(DetailView):
    template_name = 'jobs/job_detail.html'
    model = Job
