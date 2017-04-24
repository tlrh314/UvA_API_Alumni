#! /usr/bin/env python

from ..people.models import Person
import re


def tooltips():
    tooltips = {}
    for person in Person.objects.filter(show_person=True).filter(
        office__isnull=False):
        regex = re.search('(?P<office>\d{3}[a-z]?)', person.office)
        if not regex:
            continue
        office = regex.group('office')
        tooltips.setdefault(office, []).append(
            '<li>%s</li>' % person.full_name)
    tips = []
    for key, tooltip in tooltips.items():
        tips.append('<ul class="hovertip" id="tip_%s">%s</ul>' % (
            key, "\n".join(tooltip)))
    return tips
