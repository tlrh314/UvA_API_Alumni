from __future__ import unicode_literals, absolute_import, division

import xlwt
from datetime import datetime

from django.http import HttpResponse

from .models import Alumnus


def save_all_alumni_to_xls(request, queryset=None):
    xls = xlwt.Workbook(encoding='utf8')
    sheet = xls.add_sheet('API Alumni Export')

    attributes = [ "academic_title", "initials",  "first_name",  "nickname",  "middle_names",
                   "prefix", "last_name", "gender", "birth_date", "nationality",
                   "place_of_birth  ", "student_id",
                   "slug",  "email", "home_phone", "mobile",  "homepage", "facebook",
                   "twitter",  "linkedin",  "address", "streetname", "streetnumber",
                   "zipcode", "city", "country", "position", "specification", "office",
                   "work_phone", "ads_name", #"biography",  "mugshot",
                   # "research", "contact", "comments", "date_created", "date_updated",
    ]

    # Define custom styles.
    borders = xlwt.easyxf('borders: top thin, right thin, bottom  thin, left thin;')
    boldborders = xlwt.easyxf('font: bold on; borders: top thin, right thin, bottom  thin, left thin;')

    row = 0  # Create header.
    for col, attr in enumerate(attributes):
        sheet.write(row, col, attr, style=boldborders)

    if queryset:
        alumni = queryset
    else:  # used to export all alumni to Excel
        alumni = Alumnus.objects.all()

    for row, alumnus in enumerate(alumni):
        for col, attr in enumerate(attributes):
            try:
                value = str(getattr(alumnus, attr, "")).encode('ascii', 'ignore')
            except UnicodeEncodeError:
                value = "UnicodeEncodeError"

            #The formatter cannot handle bytes type classes (unicode is not evaluated in bytes). Change to unicode if necessary
            if type(value) is bytes:
                value = value.decode('unicode_escape')

            # Do some cleanups
            if value == "None": value = ""

            if attr == "student_id": value = int(value.split(".")[0]) if len(value) > 3 else ""

            if attr == 'gender':
                if not value == "":
                    value = Alumnus.GENDER_CHOICES[int(value)-1][1]

            sheet.write(row+1, col, value, style=borders)

    # # Return a response that allows to download the xls-file.
    now = datetime.now().strftime("%s" % ("%d_%b_%Y"))
    filename = u'API_Alumni_Export_{0}.xls'.format(now)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    xls.save(response)
    return response
