import os
import os.path
import shutil
import sys; sys.path.insert(0, "..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiweb.settings")

import datetime
import pickle

import django
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from apiweb.apps.people.models import Person
from apiweb.apps.alumni.models import Alumnus, Degree


def create_alumnus(first_name, nickname, middle_names, initials, prefix, last_name,
                   email, student_id):
    print("Alumnus does not yet exist, creating: ", last_name)
    alumnus = Alumnus.objects.create(
        user = User.objects.create_user(
            username=(first_name+initials+last_name).replace(" ", ""),
            password=User.objects.make_random_password(),
            first_name=first_name, last_name=last_name, email=email
        ),
        initials=initials,
        first_name=first_name,
        nickname=nickname,
        middle_names=middle_names,
        prefix=prefix,
        last_name=last_name,
        email=email,
        student_id=student_id,
    )
    alumnus.save()
    return alumnus


def add_thesis_to_alumnus(alumnus, type, date_stop, thesis_title,
        date_of_defence, thesis_url, thesis_slug, thesis_advisor):
    print("Adding MSc Thesis to Alumnus: {0}\nTitle = {1}".format(alumnus, thesis_title))
    thesis = Degree.objects.create(
            alumnus=alumnus, type=type, date_stop=date_stop,
            thesis_title=thesis_title, date_of_defence=date_of_defence,
            thesis_url=thesis_url, thesis_slug=thesis_slug, thesis_in_library=True)

    thesis.comments = "Thesis scraped from Science in Progress by D Hendriks, May 13 2017.\n"
    thesis.save()
    alumnus.save()

    thesis.thesis_advisor.add(thesis_advisor)
    thesis.save()
    alumnus.save()


def clean_scraped_theses():
    filename = "scraped_theses/grand_result_list.dump"
    grand_result_list = pickle.load(open(filename, "rb" ))
    for i, thesis_info_as_dict in enumerate(grand_result_list):
        # if i < 67: continue
        print("Eating: {0} / {1}".format(i, len(grand_result_list)))
        # for k, v in thesis_info_as_dict.items():
        #     print("{0:<25} = {1}".format(k, v))

        author_initials = thesis_info_as_dict["author_initials"]
        author_prefix = thesis_info_as_dict["author_prefix"]
        author_last_name = thesis_info_as_dict["author_last_name"]

        # AMEP
        if author_last_name == "Daiber": continue

        # Double entry, so scraped twice --> unique slug fails
        if i == 61 and author_last_name == "Maaskant": continue
        if i == 64 and author_last_name == "Rasmijn": continue
        if i == 65 and author_last_name == "Hyde": continue

        def cleandatestop(date):
            # February 14th, 2017
            month, day, year = date.split(" ")
            monthdict = {"January": 1, "February": 2, "March": 3, "April": 4,
                         "May": 5, "June": 6, "July": 7, "August": 8,
                         "September": 9, "October": 10, "November": 11, "December": 12}
            year = int(year)
            month = monthdict[month]
            for suffix in ["th,", "st,", "nd,", "rd,"]:
                day = day.replace(suffix, "")
            day = int(day)
            return(datetime.datetime(day=day, month=month, year=year))

        raw_date_stop = thesis_info_as_dict["date"]
        date_stop = cleandatestop(raw_date_stop)

        typedict = {"master": "msc", "bachelor": "bsc"}
        thesis_type = typedict.get(thesis_info_as_dict["degree_type"], "ERROR")
        thesis_title = thesis_info_as_dict["thesis_title"]
        date_of_defence = date_stop
        thesis_slug = "{0}{1}-{2}".format(author_initials.lower(),
            "-{}".format(author_prefix.lower()) if author_prefix else "",
            author_last_name.lower())
        thesis_advisor = ""

        fulltext_link = thesis_info_as_dict["fulltext_link"]
        abstract_link = thesis_info_as_dict["abstract_link"]

        # TODO: set thesis url to FNWI Science in Progress page?
        # thesis_url = "https://esc.fnwi.uva.nl/thesis/apart/phys/thesis.php?page=phys" ?
        thesis_url = fulltext_link if fulltext_link else abstract_link

        # copy files to give correct name

        print("  initials     = '{}'\n  prefix       = '{}'\n  last_name    = '{}'\n  raw_datestop = '{}'\n"
              "  date_stop    = '{}'\n  thesis_type  = '{}'\n  thesis_title = '{}'\n  date_defence = '{}'\n"
              "  thesis_url   = '{}'\n"
              "  thesis_slug  = '{}'\n  advisor      = '{}'".format(author_initials, author_prefix,
            author_last_name, raw_date_stop, date_stop, thesis_type, thesis_title, date_of_defence,
            thesis_url, thesis_slug, thesis_advisor))

        # Rename files, and set the slug correctly
        local_fulltext_location       = thesis_info_as_dict.get("local_fulltext_location", "")
        local_abstract_location       = thesis_info_as_dict.get("local_abstract_location", "")
        local_profilepicture_location = thesis_info_as_dict.get("local_profilepicture_location", "")
        local_thesispicture_location  = thesis_info_as_dict.get("local_thesispicture_location", "")

        if local_abstract_location and os.path.exists(local_abstract_location):
            abstract, ext = (local_abstract_location.split("/")[-1]).split(".")
            # shutil.copyfile(local_abstract_location, "clean/{0}-abstract.{1}".format(thesis_slug, ext))
            thesis_slug = "{0}-abstract".format(thesis_slug)

        if local_fulltext_location and os.path.exists(local_fulltext_location):
            fulltext, ext = (local_fulltext_location.split("/")[-1]).split(".")
            # shutil.copyfile(local_fulltext_location, "clean/{0}-full.{1}".format(thesis_slug, ext))
            thesis_slug = "{0}-full".format(thesis_slug)

        if local_profilepicture_location and os.path.exists(local_profilepicture_location):
            mugshot, ext = (local_profilepicture_location.split("/")[-1]).split(".")
            # shutil.copyfile(local_profilepicture_location, "clean/{0}-author.{1}".format(thesis_slug, ext))

        if local_thesispicture_location and os.path.exists(local_thesispicture_location):
            thesispicture, ext = (local_thesispicture_location.split("/")[-1]).split(".")
            # shutil.copyfile(local_thesispicture_location, "clean/{0}-thesis.{1}".format(thesis_slug, ext))

        # find supervisor
        supervisor = thesis_info_as_dict["supervisor"]
        supervisor_last_name = thesis_info_as_dict["supervisor_last_name"]
        if supervisor_last_name == "E de mink": supervisor_last_name ="Mink"
        if supervisor_last_name == "L watts": supervisor_last_name ="Watts"
        if supervisor_last_name == "Tramper msc,   l kaper": supervisor_last_name ="Kaper"
        if supervisor_last_name == "B markoff": supervisor_last_name ="Markoff"
        if supervisor_last_name == "Sb": supervisor_last_name ="Markoff"
        if supervisor_last_name == "Portegies zwart": supervisor_last_name ="Portegies Zwart"
        if supervisor_last_name == " lbfm waters": supervisor_last_name ="Waters"
        if supervisor_last_name == "Wijers & jan-pieter van der schaar": supervisor_last_name ="Wijers"
        if supervisor_last_name == "Wijnands/daniel boer (vu)": supervisor_last_name ="Wijnands"
        if author_last_name == "Velzen": supervisor_last_name ="Wijers"
        if author_last_name == "Semeijns de Vries van Doesburg": author_last_name = "Semeijns de Vries van Doesburgh"


        print("  initials     = '{}'\n  last_name    = '{}'\n".format(
            supervisor, supervisor_last_name))

        supervisor_set = Alumnus.objects.filter(last_name=supervisor_last_name)
        if supervisor_last_name == "Wijers": supervisor_set = Alumnus.objects.filter(pk=251)
        if len(supervisor_set) != 1:
            print("Please create supervisor")
            import sys; sys.exit(0)

        thesis_advisor = supervisor_set[0]
        print("  Supervisor found")
        print("     initials   =", thesis_advisor.initials.replace(".", ""))
        print("     first_name =", thesis_advisor.first_name)
        print("     last_name  =", thesis_advisor.last_name)

        alumnus_set = Alumnus.objects.filter(last_name=author_last_name)
        if not alumnus_set:
            print("Alumnus '{0}' does not exist".format(author_last_name))
            alumnus = create_alumnus("", "", "", author_initials, author_prefix, author_last_name, "", "")
            add_thesis_to_alumnus(alumnus, thesis_type, date_stop, thesis_title,
                date_of_defence, thesis_url, thesis_slug, thesis_advisor)

        if len(alumnus_set) == 1:
            alumnus = alumnus_set[0]
            add_thesis_to_alumnus(alumnus, thesis_type, date_stop, thesis_title,
                date_of_defence, thesis_url, thesis_slug, thesis_advisor)

        if len(supervisor_set) != 1:
            print("Please check alumnus")
            import sys; sys.exit(0)

if __name__ == "__main__":
    clean_scraped_theses()
