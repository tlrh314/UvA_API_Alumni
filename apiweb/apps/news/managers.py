from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.db.models import Q
from datetime import datetime, timedelta


class EventManager(models.Manager):
    """Add some event specific managers"""

    def current(self, days=None):
        """Obtain only the current (=visibile) events, in date order

        If days >= 0, this is the maximum time from now that an event
        will be returned. Ie, events past 'days' are not returned.
        Days can be negative, in which case past events up till a
        certain timespan are shown

        """

        now = datetime.now().date()
        queryset = super(EventManager, self).get_queryset().filter(
            visible=True).filter(
                date_on__lte=now).filter(date_off__gte=now).order_by('date')
        if days:
            if isinstance(days, (int, float)):
                if days > 0:
                    queryset = queryset.filter(
                        Q(date__range=(now, now+timedelta(days, 0, 0))) |
                        Q(date_end__range=(now, now+timedelta(days, 0, 0))))
                else:
                    queryset = queryset.filter(
                        Q(date__range=(now+timedelta(days, 0, 0), now)) |
                        Q(date_end__range=(now+timedelta(days, 0, 0), now)))
            elif isinstance(days, (tuple, list)) and len(days) == 2:
                queryset = queryset.filter(
                    Q(date__range=(now-timedelta(days[0], 0, 0),
                                   now+timedelta(days[1], 0, 0))) |
                    Q(date_end__range=(now-timedelta(days[0], 0, 0),
                                       now+timedelta(days[1], 0, 0))))

        else:
            queryset = queryset.filter(date__range=(
                now, now+timedelta(9999, 0, 0)))
        return queryset
