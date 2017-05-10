import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiweb.settings")

import django
django.setup()

import xlwt
from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect

from apiweb.apps.alumni.models import Alumnus
from apiweb.apps.alumni.models import Degree

# Define custom styles.
plain = xlwt.Style.default_style
borders = xlwt.easyxf('borders: top thin, right thin, bottom  thin, left thin;')
bold = xlwt.easyxf('font: bold on;')
boldborders = xlwt.easyxf('font: bold on; borders: top thin, right thin, bottom  thin, left thin;')
datetime_style = xlwt.easyxf(num_format_str='[$-413]d/mmm;@',
    strg_to_parse='borders: top thin, right thin, bottom  thin,'+
        ' left thin; font: bold on;')
#date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')


def save_all_theses_to_xls(queryset=None):
    xls = xlwt.Workbook(encoding='utf8')
    sheet = xls.add_sheet('API Theses Export')

    now = datetime.now().strftime("%s" % ("%d_%b_%Y"))
    filename = u'API_Theses_Export_{0}.xls'.format(now)

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
        print(attr)
        sheet.write(row, col+len(alumnus_attributes), attr, style=boldborders)

    xls.save(filename)
    return

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
            print(value)

        for col, attr in enumerate(attributes):
            len(alumnus_attributes)
            value = str(getattr(thesis, attr, ""))
            # Do some cleanups
            if value == "None": value = ""
            if value == "thesis_advisor": value = thesis.thesis_advisor.full_name
            sheet.write(row+1, col+len(alumnus_attributes), value, style=borders)
            print(value)
        break

    # # Return a response that allows to download the xls-file.
    now = datetime.now().strftime("%s" % ("%d_%b_%Y"))
    filename = u'API_Theses_Export_{0}.xls'.format(now)
    print(filename)


    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    # xls.save(response)
    # return response


if __name__ == "__main__":
    save_all_theses_to_xls()
