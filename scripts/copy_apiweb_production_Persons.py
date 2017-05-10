# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/home/astroweb/apiweb/api/")

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "api.settings.local"

from api.apps.people.models import Person

import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# NB this is Python 2.7
# TODO: breaks when Unicode character is detecter. Ensure unicode can be printed
print "["
for person in Person.objects.all():
    print "( ",
    print '"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}" '\
            .format(person.show_person, person.first_name, person.prefix,
            person.last_name, person.slug, person.gender,
            person.title, person.initials, person.ads_name,
            person.address, person.zipcode, person.city,
            person.country, person.home_phone, person.work_phone,
            person.mobile, person.office, person.birth_date,
            person.position, person.mugshot,
            person.photo, person.email, person.homepage,
            str([str(r) for r in person.research.all()]),
            str([str(r) for r in person.contact.all()]),
            person.comments),
    print " ),"
print "]"

