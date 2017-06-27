import os
import sys; sys.path.insert(0, "..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiweb.settings")

from datetime import datetime
import json

import django
django.setup()

from django.conf import settings
from apiweb.apps.alumni.models import Alumnus
from apiweb.apps.alumni.models import PositionType
from apiweb.apps.alumni.models import AcademicTitle
from apiweb.apps.alumni.models import PreviousPosition
from apiweb.apps.survey.models import JobAfterLeaving
from apiweb.apps.research.models import Thesis
from apiweb.apps.interviews.models import Post


with open("../dump_20170626T1629_alumni.json") as f:
    d = json.load(f)
    i = 0
    for entry in d:
        if entry["model"] == "alumni.alumnus":
            i += 1
            # if i > 10: break
            if i < 610: continue
            alumnus = Alumnus()
            alumnus.pk =  entry["pk"]
            alumnus.set_password(Alumnus.objects.make_random_password())
            alumnus.is_active = True

            alumnus.show_person = entry["fields"]["show_person"]
            alumnus.passed_away = entry["fields"]["passed_away"]
            academic_title = entry["fields"]["academic_title"]
            academic_title = AcademicTitle.objects.get(pk=academic_title) if academic_title else None
            alumnus.academic_title = academic_title
            alumnus.initials = entry["fields"]["initials"]
            alumnus.first_name= entry["fields"]["first_name"]
            alumnus.nickname = entry["fields"]["nickname"]
            alumnus.middle_names = entry["fields"]["middle_names"]
            alumnus.prefix = entry["fields"]["prefix"]
            alumnus.last_name = entry["fields"]["last_name"]
            alumnus.gender = entry["fields"]["gender"]
            birth_date = entry["fields"]["birth_date"]  # YYYY-DD-MM --> must be Date
            alumnus.birth_date = datetime.strptime(birth_date, "%Y-%m-%d") if birth_date else None
            alumnus.nationality = entry["fields"]["nationality"]  # NL --> must be CountryField?
            alumnus.place_of_birth = entry["fields"]["place_of_birth"]
            alumnus.student_id = entry["fields"]["student_id"]
            alumnus.mugshot = entry["fields"]["mugshot"]  # ImageField
            alumnus.biography = entry["fields"]["biography"]  # HTMLField
            alumnus.email = entry["fields"]["email"]
            alumnus.home_phone = entry["fields"]["home_phone"]
            alumnus.mobile = entry["fields"]["mobile"]
            alumnus.homepage = entry["fields"]["homepage"]
            alumnus.facebook = entry["fields"]["facebook"]
            alumnus.twitter = entry["fields"]["twitter"]
            alumnus.linkedin = entry["fields"]["linkedin"]
            last_checked = entry["fields"]["last_checked"]  # 2017-05-18T13:28:59 --> DateTime
            last_checked = last_checked[:-4] if last_checked and "." in last_checked else last_checked
            alumnus.last_checked = datetime.strptime(last_checked, "%Y-%m-%dT%H:%M:%S") if last_checked else None
            alumnus.address = entry["fields"]["address"]
            alumnus.streetname = entry["fields"]["streetname"]
            alumnus.streetnumber = entry["fields"]["streetnumber"]
            alumnus.zipcode = entry["fields"]["zipcode"]
            alumnus.city = entry["fields"]["city"]
            alumnus.country = entry["fields"]["country"]  # CountryField
            position = entry["fields"]["position"]
            alumnus.position = PositionType.objects.get(pk=position) if position else None
            alumnus.specification = entry["fields"]["specification"]
            alumnus.office = entry["fields"]["office"]
            alumnus.work_phone = entry["fields"]["work_phone"]
            alumnus.ads_name = entry["fields"]["ads_name"]
            alumnus.comments = entry["fields"]["comments"]
            alumnus.last_updated_by = None
            date_created = entry["fields"]["date_created"]  # 2017-05-14T13:02:40.785 --> DateTime
            date_created = date_created[:-4] if date_created and "." in date_created else date_created
            alumnus.date_created = datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%S") if date_created else None
            date_updated = entry["fields"]["date_updated"]  # 2017-05-22T10:33:26.177 --> DateTime
            date_updated = date_updated[:-4] if date_updated and "." in date_updated else date_updated
            alumnus.date_updated = datetime.strptime(date_updated, "%Y-%m-%dT%H:%M:%S") if date_updated else None
            alumnus.show_biography = entry["fields"]["show_biography"]
            alumnus.show_facebook = entry["fields"]["show_facebook"]
            alumnus.show_linkedin = entry["fields"]["show_linkedin"]
            alumnus.show_twitter = entry["fields"]["show_twitter"]
            alumnus.show_email = entry["fields"]["show_email"]
            alumnus.show_homepage = entry["fields"]["show_homepage"]

            alumnus.username = alumnus.full_name_no_title.replace(" ", "")
            # Slug is autogenerated on save
            # alumnus.slug = entry["fields"]["slug"]

            if alumnus.last_name == "Halbesma" or alumnus.last_name == "Hendriks":
                alumnus.is_active = True
                alumnus.is_staff = True
                alumnus.is_superuser = True

            alumnus.save()
            print(alumnus)
            print(alumnus.slug)
            print(alumnus.username)
            print(alumnus.pk)
            print()

