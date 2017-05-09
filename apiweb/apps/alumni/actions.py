import xlwt
from datetime import datetime

from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect

from .models import Alumnus
from .models import Degree

# Define custom styles.
plain = xlwt.Style.default_style
borders = xlwt.easyxf('borders: top thin, right thin, bottom  thin, left thin;')
bold = xlwt.easyxf('font: bold on;')
boldborders = xlwt.easyxf('font: bold on; borders: top thin, right thin, bottom  thin, left thin;')
datetime_style = xlwt.easyxf(num_format_str='[$-413]d/mmm;@',
    strg_to_parse='borders: top thin, right thin, bottom  thin,'+
        ' left thin; font: bold on;')
#date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')


def save_all_alumni_to_xls(request, queryset=None):
    xls = xlwt.Workbook(encoding='utf8')
    sheet = xls.add_sheet('API Alumni Export')

    attributes = [ "title", "initials",  "first_name",  "nickname",  "middle_names",
                   "prefix", "last_name", "gender", "birth_date", "nationality",
                   "place_of_birth  ", "student_id",
                   "slug",  "email", "home_phone", "mobile",  "homepage", "facebook",
                   "twitter",  "linkedin",  "address", "streetname", "streetnumber",
                   "zipcode", "city", "country", "position", "specification", "office",
                   "work_phone", "ads_name", #"biography",  "mugshot", "photo",
                   # "research", "contact", "comments", "date_created", "date_updated",
    ]

    row = 0  # Create header.
    for col, attr in enumerate(attributes):
        sheet.write(row, col, attr, style=boldborders)

    if queryset:
        alumni = queryset
    else:  # used to export all alumni to Excel
        alumni = Alumnus.objects.all()

    for row, alumnus in enumerate(alumni):
        for col, attr in enumerate(attributes):
            value = str(getattr(alumnus, attr, ""))
            # Do some cleanups
            if value == "None": value = ""
            if attr == "student_id": value = int(value.split(".")[0]) if len(value) > 3 else ""
            if attr == "gender": value = int(value) if value != "" else ""
            sheet.write(row+1, col, value, style=borders)

    # # Return a response that allows to download the xls-file.
    now = datetime.now().strftime("%s" % ("%d_%b_%Y"))
    filename = u'API_Alumni_Export_{0}.xls'.format(now)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    xls.save(response)
    return response


def save_all_theses_to_xls(request, queryset=None):
    xls = xlwt.Workbook(encoding='utf8')
    sheet = xls.add_sheet('API Theses Export')

    alumnus_attributes = [ "title", "initials",  "first_name",  "nickname",
        "middle_names", "prefix", "last_name", "gender" ]
    attributes = [ "type", "date_start", "date_stop", "thesis_title",
                   "date_of_defence", "thesis_url", "thesis_slug", "thesis_advisor",
                   "thesis_in_library",
    ]

    row = 0  # Create header.
    for col, attr in enumerate(alumnus_attributes):
        sheet.write(row, col, attr, style=boldborders)
    for col, attr in enumerate(attributes):
        sheet.write(row, col+len(alumnus_attributes), attr, style=boldborders)

    if queryset:
        theses = queryset
    else:  # used to export all theses to Excel
        theses = (Degree.objects.filter(type="phd").order_by("-date_of_defence")
            |  Degree.objects.filter(type="msc").order_by("alumnus__last_name"))

    for row, thesis in enumerate(theses):
        for col, attr in enumerate(alumnus_attributes):
            value = str(getattr(thesis.alumnus, attr, ""))
            # Do some cleanups
            if value == "None": value = ""
            sheet.write(row+1, col, value, style=borders)

        for col, attr in enumerate(attributes):
            len(alumnus_attributes)
            value = str(getattr(thesis, attr, ""))
            # Do some cleanups
            if value == "None": value = ""
            if attr == "thesis_advisor" and "None" in value: value = ""
            sheet.write(row+1, col+len(alumnus_attributes), value, style=borders)

    # # Return a response that allows to download the xls-file.
    now = datetime.now().strftime("%s" % ("%d_%b_%Y"))
    filename = u'API_Theses_Export_{0}.xls'.format(now)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    xls.save(response)
    return response
