import os
import sys; sys.path.insert(0, "..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiweb.settings")

import datetime

import xlwt
import xlrd
import json
import string
import os.path

import django
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from apiweb.apps.people.models import Person
from apiweb.apps.alumni.models import Alumnus,PreviousPosition, PositionType


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


def add_position_to_alumnus(alumnus, date_start, date_stop, cleanposition, cleannova,
                            cleanfunding, funding_note, funding_remark,fte_per_year):
    prevpos = PreviousPosition.objects.create(
            alumnus=alumnus, date_start=date_start, date_stop=date_stop,
            type=cleanposition, nova=cleannova, funding=cleanfunding, funding_note=funding_note,
            funding_remark=funding_remark,fte_per_year=fte_per_year)

    prevpos.comments = "PreviousPosition automatically read-in by TLR Halbesma, May 11 2017.\n"
    prevpos.save()
    alumnus.save()

    return prevpos



def add_info_from_astronomers_in_the_netherlands():
    path_to_data_xlsx = "../apiweb/databases/Astronomers_In_The_Netherlands.xlsx"

    if not os.path.exists(path_to_data_xlsx):
        print("ERROR: '{0}' does not exist".format(path_to_data_xlsx))
        return

    book = xlrd.open_workbook(path_to_data_xlsx)

    # Sheets are RUG, UvA, UL, UU, RU, Symmary, Funding, Age
    sheet = book.sheet_by_index(1)
    print("Opened file: ", path_to_data_xlsx)

    def clean(str):
        if str[0:2] == "  ":
            return str[2:]
        elif str == "":
            return str
        else:
            print(str)
            raise IntegrityError("Data incorrect")

    # Header lives on row 0. Columns are:
    # Naam, Naam2, Birth, functie, M/V, NW1, NW2, NW3, Instr, fte, instituut, funding, Note, remark, start, eind
    # Further colums contain number of fte per year from 1995 to 2021
    for row_nr in range(1, sheet.nrows):
        if row_nr > 421: break
        # if row_nr < 412: continue
        print("Eating: {0} / {1}".format(row_nr, sheet.nrows-1))

        # Eat all columns up to list of fte per year
        full_name, last_name, birth_year, functie, gender, nova1, nova2, nova3, instrumentation, \
            fte, instituut, funding, note, remark, date_start, date_stop = \
                [sheet.cell_value(row_nr, col_nr) for col_nr in range(16)]


        # Eat and json fte per year
        fte_per_year = {year: sheet.cell_value(row_nr, col+16) for col, year in enumerate(range(1995, 2022))}

        # Print the uncleaned data
        # print("  full_name   = '{}'\n  last_name   = '{}'\n  birth_year  = '{}'\n  functie     = '{}'\n"
        #       "  gender      = '{}'\n  nova1       = '{}'\n  nova2       = '{}'\n  nova3       = '{}'\n"
        #       "  instrument. = '{}'\n  fte         = '{}'\n  instituut   = '{}'\n  funding     = '{}'\n"
        #       "  note        = '{}'\n  remark      = '{}'\n  date_start  = '{}'\n  date_stop   = '{}'\n"\
        #           .format(full_name, last_name, birth_year, functie, gender, nova1, nova2, nova3,
        #                   instrumentation, fte, instituut, funding, note, remark, date_start, date_stop))

        def cleanbirth(year):
            return int(year) if year != "" else None
        def cleandate(date):
            return datetime.datetime(*xlrd.xldate_as_tuple(date, book.datemode)) if type(date) is float else None
        def cleannova(nova):
            return True if nova == 1.0 else False
        def cleangender(gender):
            return { "M": 1, "V": 2 }.get(gender, 3)   # Alumnus.GENDER_CHOICES
        def cleanfullname(name):
            titles = ["Prof.dr.", "Dr.", "Drs.", "MSc"]
            for t in titles:
                if t in name:
                    title = t
                    name = name.replace(title+" ", "")
                    name = name.replace(" "+title, "")  # for MSc
                    break
            else:
                title = ""
            number_of_initials = name.count(".")
            namelist = name.split(".")
            initials = "".join(str(i).strip() for i in namelist[0:number_of_initials])
            name = "".join(str(i).strip() for i in namelist[number_of_initials:])
            if name == "Semeijns de Vries van Doesburgh":
                prefix = ""
            else:
                for p in ["in 't", "di", "de", "van", "van der", "van den", "der", "den"]:
                    if p+" " in name:
                        prefix = p
                        name = name.replace(p, "")
                        break
                else:
                    prefix = ""
            print("Title    =", title)
            print("Initials =", initials)
            print("Prefix   =", prefix)
            print("Name     =", name)
            return title, initials, prefix, name


        # Clean
        full_name, last_name, birth_year, functie, gender, nova1, nova2, nova3,\
        instrumentation, fte, instituut, funding, note, remark, date_start, date_stop = \
            full_name, last_name, cleanbirth(birth_year), functie, cleangender(gender),\
            cleannova(nova1), cleannova(nova2), cleannova(nova3), cleannova(instrumentation),\
            float(fte) if fte != "" else None, instituut, funding, note, remark,\
            cleandate(date_start), cleandate(date_stop)

        def getnova(*novalist):
            # print(PreviousPosition.NOVA_NETWORK)
            nova = [i+1 for (i, nova) in enumerate(novalist) if nova]
            if len(nova) != 1:
                print("More than one nova network. Nova =", nova)
                return None
            else:
                return {1: "NW1", 2: "NW2", 3: "NW3", 4: "INS" }.get(nova[0], 9)

        def getfunding(fund):
            # print(PreviousPosition.FUNDING)
            d = dict(PreviousPosition.FUNDING)
            ivd = {v: k for k, v in d.items()}
            return (ivd.get(fund, "ERROR"))

        def getposition(pos):
            # TODO: ask Annemarie which positions there are, and what the abbreviations mean in the column 'functie'
            posdict = {"staff": "Faculty Staff",
                       "HL": "Full Professor",
                       "co-work": "Adjunct Staff",
                       "research": "Research Staff",
                       "em": "Emeritus",
                       "OBP": "OBP",
                       "Proj.Man.": "Nova",
                       "Comm.Adv.": "Nova",
                       "Comm. Adv.": "Nova",
                       "comm. Adv.": "Nova",
                       "inst. Coordinator": "Institute Manager",
                       "Inst.Coordinator": "Institute Manager",
                       "Comm. Medew.": "Outreach",
                       "comp": "Software Developer",
                       "secr.": "Secretary",
                       "docent": "Teacher",
                       "bedrijfsvoerder": "Institute Manager",
                       "Bedrijfsvoerder": "Institute Manager",
                       "Instr": "Instrumentation",
                       "pd": "Postdoc",
                       "aio": "PhD Student" }
            posname = posdict.get(pos, None)
            return PositionType.objects.filter(name=posname)[0]

        cleanposition = getposition(functie)
        cleannova = getnova([nova1, nova2, nova3, instrumentation])
        cleanfunding = getfunding(funding)

        # Print the cleaned data
        print("  full_name   = '{}'\n  last_name   = '{}'\n  birth_year  = '{}'\n  functie     = '{}'\n"
              "  gender      = '{}'\n  nova1       = '{}'\n  nova2       = '{}'\n  nova3       = '{}'\n"
              "  instrument. = '{}'\n  fte         = '{}'\n  instituut   = '{}'\n  funding     = '{}'\n"
              "  note        = '{}'\n  remark      = '{}'\n  date_start  = '{}'\n  date_stop   = '{}'\n"
              "  novaclean   = '{}'\n  fundingclean= '{}'\n  position    = '{}'\n".format(full_name,
                  last_name, birth_year, functie, gender, nova1, nova2, nova3, instrumentation, fte,
                  instituut, funding, note, remark, date_start, date_stop, cleannova, cleanfunding, cleanposition))
        print(fte_per_year)

        # print(json.dumps(fte_per_year))

        alumnus_set = Alumnus.objects.filter(last_name=last_name)
        degeneracy_fix = { "Wijers": 251, "Berg": 19, "Russell": 205,
                "Bouwman": 357, "Groot": 355, "Homan": 482, "Vries": 244}

        if len(alumnus_set) == 2:
            pk = degeneracy_fix.get(last_name, None)
            if pk :
                alumnus_set = Alumnus.objects.filter(pk=pk)

        if not alumnus_set:
            title, initials, prefix, last_name = cleanfullname(full_name)
            alumnus = create_alumnus("", "", "", initials, prefix, last_name, "", "")
            alumnus.gender = gender
            add_position_to_alumnus(alumnus, date_start, date_stop, cleanposition,
                                    cleannova, cleanfunding, note, remark, fte_per_year)
        elif len(alumnus_set) == 1:
            alumnus = alumnus_set[0]
            add_position_to_alumnus(alumnus, date_start, date_stop, cleanposition,
                                    cleannova, cleanfunding, note, remark, fte_per_year)
        else:
            match_found = False
            for i, alumnus in enumerate(alumnus_set):
                print("  Alumnus {0}:".format(i))
                print("     initials   =", alumnus.initials.replace(".", ""))
                print("     first_name =", alumnus.first_name)
                print("     last_name  =", alumnus.last_name)

                confirm = input("Correct Alumnus? [Yy]")
                if confirm.lower() == "y":
                    add_position_to_alumnus(alumnus, date_start, date_stop, cleanposition,
                                            cleannova, cleanfunding, note, remark, fte_per_year)
                    match_found = True
                    break
                else:
                    print("Info not added")

            if match_found:
                continue
            else:
                print("Match not found")

                title, initials, prefix, last_name = cleanfullname(full_name)
                alumnus = create_alumnus("", "", "", initials, prefix, last_name, "", "")
                alumnus.gender = gender
                alumnus.save()
                add_position_to_alumnus(alumnus, date_start, date_stop, cleanposition,
                                        cleannova, cleanfunding, note, remark, fte_per_year)
                continue


if __name__ == "__main__":
    add_info_from_astronomers_in_the_netherlands()
