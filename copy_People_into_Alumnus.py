import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiweb.settings")

import datetime

import xlwt
import xlrd
import string
import os.path

import django
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from apiweb.apps.people.models import Person
from apiweb.apps.alumni.models import Alumnus, CurrentPosition
from apiweb.apps.alumni.models import Degree
from apiweb.apps.research.models import ResearchTopic, Thesis


def copy_People_to_Alumnus():
    """ This function eats all existing people.Person instances, cleans all
        fields and copies the data into the relevant alumnus.Alumnus field """

    person_count = Person.objects.count()
    i = 0
    for person in Person.objects.all():
        print("Copying: {0}".format(person))
        print("Count: {0} / {1}".format(i, person_count))
        i += 1

        # Create new instance of Alumnus, copy data from person
        alumnus, created = Alumnus.objects.get_or_create(user=person.user)
        alumnus.save()
        # Save creates an id; otherwise Research ManyToMany cannot be saved.

        # Fields already known. TODO: clean this up
        alumnus.user            =     person.user
        alumnus.show_person     =     True
        alumnus.first_name      =     person.first_name
        alumnus.prefix          =     person.prefix
        alumnus.last_name       =     person.last_name
        alumnus.title           =     person.title
        alumnus.initials        =     person.initials.replace(".", "")
        alumnus.gender          =     person.gender
        alumnus.birth_date      =     person.birth_date
        # TODO: if not person.show_person then probably photo (very) old / outdated
        alumnus.mugshot         =     person.mugshot
        alumnus.photo           =     person.photo
        alumnus.slug            =     person.slug
        # TODO: if not person.show_person then probably UvANetID@UvA.nl and no longer valid.
        alumnus.email           =     person.email
        alumnus.home_phone      =     person.home_phone
        alumnus.mobile          =     person.mobile
        # TODO: curl homepage to check if this exists?
        alumnus.homepage        =     person.homepage
        # TODO: if not person.show_person then probably alumnus, thus, address likely no longer valid.
        alumnus.address         =     person.address
        alumnus.zipcode         =     person.zipcode
        alumnus.city            =     person.city
        alumnus.country         =     person.country
        alumnus.specification   =     person.specification
        alumnus.office          =     person.office
        alumnus.work_phone      =     person.work_phone
        # TODO: should ads_name really be a separate field? This could be class method if name and initials known
        alumnus.ads_name        =     person.ads_name

        # TODO: Stalk alumni on the social media.
        # alumnus.linkedin        =
        # alumnus.facebook        =
        # alumnus.twitter         =

        # Further fields added by David
        # alumnus.nationality     =     person.nationality
        # alumnus.place_of_birth  =     person.place_of_birth

        alumnus.save()
        for research_interest in person.research.all():
            alumnus.research.add(research_interest)
        for research_contactperson in person.contact.all():
            alumnus.contact.add(research_contactperson)

        """ Done, save, and next #loveit :) """
        alumnus.save()
        print("Done")
        # break


POSITION = {
    'DIRECTOR': 1,
    'STAFF': 2,
    'NOVA': 3,
    'ADJUNCT': 4,
    'POSTDOC': 5,
    'PHD': 6,
    'EMERITUS': 7,
    'GUEST': 8,
    'MASTER': 9,
    'BACHELOR': 10,
    'DEVELOPER': 11}
POSITION_OPTIONS = (
    (POSITION['DIRECTOR'], _("Director")),
    (POSITION['STAFF'], _("Faculty Staff")),
    (POSITION['NOVA'], _("Nova")),
    (POSITION['ADJUNCT'], _("Adjunct Staff")),
    (POSITION['POSTDOC'], _("Postdoc")),
    (POSITION['PHD'], _("PhD Student")),
    (POSITION['EMERITUS'], _("Emeritus")),
    (POSITION['GUEST'], _("Guest")),
    (POSITION['MASTER'], _("Master Student")),
    (POSITION['BACHELOR'], _("Bachelor Student")),
    (POSITION['DEVELOPER'], _("Software Developer")),
)


def create_position_instances():
    for p in POSITION_OPTIONS:
        position_name = p[1]
        print(position_name)

        position, created = CurrentPosition.objects.get_or_create(
            name=position_name,
            plural=position_name+"s" if position_name != "Emeritus" else "Emeriti" )
        position.save()


def convert_old_position(position_integer):
    position_name = dict(POSITION_OPTIONS)[position_integer]
    position = CurrentPosition.objects.filter(name=position_name)
    print(position)
    return position


def add_info_from_latest_production_dump():
    # new_position_instance = convert_old_position(integerrrr)
    # prefix, position, title, first_name, initials, last_name, gender, email, address, country, home_phone, mobile, homepage, mugshot, office, photo, show_person, slug

    #    for position in person.position.all():
    #        alumnus.position.add(position)

    pass




# Helper functions to generate column names (A-Z, AA-ZZ, etc) for Excel
def base_26_gen(x):
    if x == 0: yield x
    while x > 0:
        yield x % 26
        x //= 26

def base_26_chr(x):
    return ''.join(string.uppercase[i] for i in reversed(list(base_26_gen(x))))

def get_excel_col_names(x):
    # fails for aa, ab, .., az because a is treated as a zero
    col_names = [base_26_chr(x) for x in range(x)]

    # add aa, ab, .., az in the utmost ugly way possible.
    aa_trough_az = ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', \
            'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS',\
            'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ']
    if x < 26:
        result = col_names[0:x+1]
    elif x < 52:
        result = col_names[0:26] + aa_trough_az[0:(x-25)]
    else:
        result = col_names[0:26] + aa_trough_az + col_names[26:x-25]
    return result


def clean_year(year):
    """ @param year: string, either YYYY or YYYYMMDD
        @return: DateTime object that can be stored in database """

    if type(year) == float:
        year = str(int(year))

    if len(year) == 4:
        return datetime.datetime(year=int(year), month=1, day=1)
    elif len(year) == 8:
        cleanyear = int(year[0:4])
        cleanmonth = int(year[4:6])
        cleanday = int(year[6:8])
        return datetime.datetime(year=cleanyear, month=cleanmonth, day=cleanday)


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


def add_msc_thesis_to_alumnus(alumnus, year_start, year, thesis_title, in_library,
                              comments, supervisor=None):
    print("Adding MSc Thesis to Alumnus: {0}\nTitle = {1}".format(alumnus, thesis_title))
    degree = Degree.objects.create(
        alumnus=alumnus,
        type="msc",
        date_start=clean_year(year_start),
        date_stop=clean_year(year),
        thesis_title=thesis_title,
        date_of_defence=clean_year(year),
        thesis_in_library=in_library,
        comments=comments,
    )
    degree.save()
    alumnus.save()
    print("Done\n")


def add_list_of_masterstudents_with_thesistitle():
    """ Eat the (already cleaned) list of MSc Theses at API. This Excel sheet
        sent by Annemarie spans 1956 - current (d.d. 20170405) """

    path_to_msc_theses_xlsx = "apiweb/databases/API_MSc_overzicht_CLEAN.xlsx"
    if not os.path.exists(path_to_msc_theses_xlsx):
        print("ERROR: '{0}' does not exist".format(path_to_msc_theses_xlsx))
        return

    book = xlrd.open_workbook(path_to_msc_theses_xlsx)
    sheet = book.sheet_by_index(0)
    print("Opened file: ", path_to_msc_theses_xlsx)

    # Header lives on row 0. Columns are:
    # Type, First Name, Roepnaam, Middle Names, Initials, Infix, Last Name, Email,
    # Student ID, Thesis Title, Year Start, Year, Supervisor, In library?, Comments
    # Note that infix=prefix
    for row_nr in range(1, sheet.nrows):
        # for col_nr in range(sheet.ncols):
        #     print(sheet.cell_value(row_nr, col_nr), end=', ')
        # break

        # Ignore the type string because this is useless
        # type_string  = sheet.cell_value(row_nr, 0)
        print("Eating: {0} / {1}".format(row_nr, sheet.nrows-1))
        type_string = "API MSc Student"
        first_name   = sheet.cell_value(row_nr, 1)
        nickname     = sheet.cell_value(row_nr, 2)
        middle_names = sheet.cell_value(row_nr, 3)
        initials     = sheet.cell_value(row_nr, 4)
        prefix       = sheet.cell_value(row_nr, 5)
        last_name    = sheet.cell_value(row_nr, 6)
        email        = sheet.cell_value(row_nr, 7)
        student_id   = sheet.cell_value(row_nr, 8)
        thesis_title = sheet.cell_value(row_nr, 9)
        year_start   = sheet.cell_value(row_nr, 10)
        year         = sheet.cell_value(row_nr, 11)
        supervisor   = sheet.cell_value(row_nr, 12)
        in_library   = True if sheet.cell_value(row_nr, 13) == "Y" else False
        comments     = sheet.cell_value(row_nr, 14)

        print("  type_string  = {0}\n  first_name   = {1}\n  nickname     = {2}\n  "
              "middle_names = {3}\n  initials     = {4}\n  prefix       = {5}\n  "
              "last_name    = {6}\n  email        = {7}\n  student_id   = {8}\n  "
              "thesis_title = {9}\n  year_start   = {10}\n  year         = {11}\n  "
               "supervisor   = {12}\n  in_library   = {13}\n  comments     = {14}"
                    .format(type_string, first_name,
            nickname, middle_names, initials, prefix, last_name, email,
            student_id, thesis_title, year_start, year, supervisor,
            in_library, comments)
        )

        alumnus_set = Alumnus.objects.filter(last_name=last_name)
        if not alumnus_set:
            # Alumnus does not exist, so create and add thesis.
            alumnus = create_alumnus(first_name, nickname, middle_names, initials, prefix,
                last_name, email, student_id)
            add_msc_thesis_to_alumnus(alumnus, year_start, year,
                thesis_title, in_library, comments, supervisor=None)
            continue

        print("We have {0} matching Alumnus candidates.".format(alumnus_set.count()))
        i = 0
        match_found = False
        for alumnus in alumnus_set:
            i += 1
            print("  Alumnus {0}:".format(i))
            print("     initials   =", alumnus.initials.replace(".", ""))
            print("     first_name =", alumnus.first_name)
            print("     last_name  =", alumnus.last_name)

            if alumnus.initials.replace(".", "") == initials:
                print("  Match found with Alumnus", i)
                msc_degree = alumnus.degrees.filter(type="msc")
                if not msc_degree:
                    add_msc_thesis_to_alumnus(alumnus, year_start, year,
                        thesis_title, in_library, comments, supervisor=None)
                    match_found = True
                    break
                elif len(msc_degree) == 1:
                    if msc_degree[0].thesis_title == thesis_title:
                        print("Thesis was already added, we're good. Done\n")
                        match_found = True
                        break
                    else:
                        pass
                        # check year, but year could be empty...
                        # thesisdate = msc_degree[0].date_stop.strftime("%Y-%m-%d")
                        #    thesisdate == clean_year(year).strftime("%Y-%m-%d")
                else:
                    print("Houston, we have a problem")
                    exit(0)
            else:
                print("Special case: mitsmatch in initials, but only one last_name match.")
                confirm = input("Add thesis anyway? [Yy]")
                if confirm.lower() == "y":
                    add_msc_thesis_to_alumnus(alumnus, year_start, year,
                        thesis_title, in_library, comments, supervisor=None)
                    match_found = True
                    break
                else:
                    print("Thesis not added")

        if match_found:
            continue
        else:
            print("Match not found")
            alumnus = create_alumnus(first_name, nickname, middle_names, initials,
                prefix, last_name, email, student_id)
            add_msc_thesis_to_alumnus(alumnus, year_start, year, thesis_title, in_library,
                comments, supervisor=None)
            continue
        return



def add_phd_thesis_to_alumnus(alumnus, thesis_title, defence_date,
                             thesis_url, thesis_slug, gender):
    print("Adding PhD Thesis to Alumnus: {0}\nTitle = {1}".format(alumnus, thesis_title))
    degree = Degree.objects.create(
        alumnus=alumnus,
        type="phd",
        date_stop=defence_date,
        date_of_defence=defence_date,
        thesis_title=thesis_title,
        thesis_url=thesis_url,
        thesis_slug=thesis_slug,
        thesis_in_library=True,
    )

    alumnus.gender = gender
    degree.save()
    alumnus.save()
    print("Done\n")


def add_research_dot_models_dot_Thesis_to_Alumnus():
    thesiscount = -1
    for thesis in Thesis.objects.all():
        thesiscount += 1
        print("Eating: {0} / {1}".format(thesiscount, Thesis.objects.count()))
        authorsplit = thesis.author.split(" ")
        initials = authorsplit[0].replace(".", "")
        prefix = ""
        if authorsplit[1] in ["van", "de", "den", "der"]:
            prefix += authorsplit[1]
            if authorsplit[2] in ["der", "den", "de"]:
                prefix += " " + authorsplit[2]
                authorsplit = authorsplit[2:]
            else:
                authorsplit = authorsplit[1:]
        last_name = " ".join(authorsplit[1:])  # In case of double last_name

        # print("author       =", thesis.author)
        print("initials     =", initials)
        print("prefix       =", prefix)
        print("last_name    =", last_name)
        print("gender       =", thesis.gender)
        print("title        =", thesis.title)
        print("defence date =", thesis.date)
        print("type         =", thesis.type)
        print("url          =", thesis.url)
        print("slug         =", thesis.slug)

        alumnus_set = Alumnus.objects.filter(last_name=last_name)
        # Easy case: empty QuerySet means Alumnus does not exist yet, so created it.
        if not alumnus_set:
            print("Alumnus does not exist yet. Create instance.")
            alumnus = create_alumnus("", "", "", initials,
                prefix, last_name, "", "")
            add_phd_thesis_to_alumnus(alumnus, thesis.title, thesis.date,
                thesis.url, thesis.slug, thesis.gender)
            print("New Alumnus created, thesis added. Done\n")
            continue
        elif len(alumnus_set) == 1:
            alumnus = alumnus_set[0]
            print("Alumnus does exist")
            print("  initials   =", alumnus.initials.replace(".", ""))
            print("  first_name =", alumnus.first_name)
            print("  last_name  =", alumnus.last_name)

            try:
                if(alumnus.degree.title_of_thesis == thesis.title):
                    print("We already added the thesis to existing Alumnus. Done\n")
                    continue
                else:
                    print("Alumnus does have a Degree, but title does not match.")
                    print("Dunno why")
                    return
            except Degree.DoesNotExist as e:
                print("Degree DoesNotExist")
                if str(e) == "Alumnus has no degree.":
                    add_phd_thesis_to_alumnus(alumnus, thesis.title,
                        thesis.date, thesis.url, thesis.slug, thesis.gender)
                    print("Thesis added to existing Alumnus. Done\n")
                    continue
                else:
                    raise
        elif len(alumnus_set) > 1:
            print("We have {0} matching Alumnus instances.".format(alumnus_set.count()))
            i = -1
            match_found = False
            for alumnus in alumnus_set:
                i += 1
                print("  Alumnus {0}:".format(i))
                print("     initials   =", alumnus.initials.replace(".", ""))
                print("     first_name =", alumnus.first_name)
                print("     last_name  =", alumnus.last_name)

                if alumnus.initials.replace(".", "") == initials:
                    print("  Match found with Alumnus", i)
                try:
                    if(alumnus.phd.phd_thesis.title == thesis.title):
                        print("We already added the thesis to existing Alumnus. Done\n")
                        match_found = True
                        break
                    else:
                        print("Alumnus does have a Degree, but title does not match.")
                        print("Dunno why")
                        return
                except Degree.DoesNotExist as e:
                    print("Degree DoesNotExist")
                    if str(e) == "Alumnus has no degree.":
                        add_phd_thesis_to_alumnus(alumnus, thesis.title,
                            thesis.date, thesis.url, thesis.slug, thesis.gender)
                        print("Thesis added to existing Alumnus. Done\n")
                        match_found = True
                        break
                    else:
                        raise

                if match_found:
                    continue
                else:
                    print("Match not found")
                    alumnus = create_alumnus("", "", "",
                        initials, prefix, last_name, "", "")
                    add_msc_thesis_to_alumnus(alumnus, year_start, year, thesis_title, in_library,
                        comments, supervisor=None)
                    print("New Alumnus created, thesis added. Done\n")
                    continue
                return


if __name__ == "__main__":
    # Gather data already present in existing API website
    # copy_People_to_Alumnus()
    # add_list_of_masterstudents_with_thesistitle()
    # add_research_dot_models_dot_Thesis_to_Alumnus()
    # create_position_instances()
    # add_info_from_latest_production_dump()

    # Probably has to be done manually
    # TODO: biography lives in Milena's pdf and can be copy-pasted lol.
    # alumnus.biography       =     person.biography


    exit()
    # Clean stuff. Mobile not only has the occasional "-" or "+", but also "(0)" and sometimes more than one number with an ascii explanation
    for a in Alumnus.objects.all():
        # TODO: Enforce that phone numbers are digits only, without hypens or any other formatting
        if a.mobile:
            print(a.mobile.replace("-","").replace("+","00").strip())
        if a.home_phone:
            print(a.home_phone.replace("-","").replace("+","00").strip())

        # TODO: split address up into streetname and streetnumber and clean up zipcode
        # alumnus.streetname      =
        # alumnus.streetnumber    =

        # TODO: Ensure city and country name is all same format, not mixture of ([Tt]he) [Nn]etherlands, Holland
        # This is probably going to be most tricky and perhaps must be done by hand
