from __future__ import unicode_literals, absolute_import, division

import xlwt
from datetime import datetime

from django.http import HttpResponse

from .models import Thesis
from ..alumni.models import Alumnus


def save_all_theses_to_xls(request, queryset=None):
    xls = xlwt.Workbook(encoding='utf8')
    sheet = xls.add_sheet('API Theses Export')

    alumnus_attributes = [ "academic_title", "initials",  "first_name",  "nickname",
        "middle_names", "prefix", "last_name", "gender" ]
    attributes = [ "type", "date_start", "date_stop", "title", "date_of_defence",
        "url", "slug", "advisor", "in_library",
    ]

    # Define custom styles.
    borders = xlwt.easyxf('borders: top thin, right thin, bottom  thin, left thin;')
    boldborders = xlwt.easyxf('font: bold on; borders: top thin, right thin, bottom  thin, left thin;')

    row = 0  # Create header.
    for col, attr in enumerate(alumnus_attributes):
        sheet.write(row, col, attr, style=boldborders)
    for col, attr in enumerate(attributes):
        sheet.write(row, col+len(alumnus_attributes), attr, style=boldborders)

    if queryset:
        theses = queryset
    else:  # used to export all theses to Excel
        theses = (Thesis.objects.filter(type="phd").order_by("-date_of_defence")
            |  Thesis.objects.filter(type="msc").order_by("alumnus__last_name"))

    for row, thesis in enumerate(theses):
        for col, attr in enumerate(alumnus_attributes):
            try:
                if (attr == 'last_name') or (attr == 'first_name'):
                    value = str(getattr(thesis.alumnus, attr, ""))
                else:
                    value = str(getattr(thesis.alumnus, attr, u"")).encode('ascii', 'ignore')
            except UnicodeEncodeError:
                value = "UnicodeEncodeError"

            #The formatter cannot handle bytes type classes (unicode is not evaluated in bytes). Change to unicode if necessary
            if type(value) is bytes:
                value = value.decode('unicode_escape')

            # Do some cleanups
            if value == "None": value = ""

            if attr == 'gender':
                if not value == "":
                    value = Alumnus.GENDER_CHOICES[int(value)-1][1]

            sheet.write(row+1, col, value, style=borders)

        for col, attr in enumerate(attributes):
            try:
                value = str(getattr(thesis, attr, u"")).encode('ascii', 'ignore')

            except UnicodeEncodeError:
                value = "UnicodeEncodeError"

            #Need custom way to do this as the normal method gives strange errors
            if attr == "advisor":
                if not len(str(thesis)) == 0:
                    res = Thesis.objects.filter(title=thesis)[0].advisor.all()
                    advisors_list = []
                    for advisor in res:
                        string = "'" + str(advisor.full_name) + "'"
                        advisors_list.append(string)
                    advisors_string = ', '.join(advisors_list)
                    value = advisors_string
                else:
                    value = ""

            if attr == "slug":
                if len(str(thesis)) == 0:
                    value = ""

            #The formatter cannot handle bytes type classes (unicode is not evaluated in bytes). Change to unicode if necessary
            if type(value) is bytes:
                value = value.decode('unicode_escape')

            # Do some cleanups
            if value == "None": value = ""

            sheet.write(row+1, col+len(alumnus_attributes), value, style=borders)

    # # Return a response that allows to download the xls-file.
    now = datetime.now().strftime("%s" % ("%d_%b_%Y"))
    filename = u'API_Theses_Export_{0}.xls'.format(now)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    xls.save(response)
    return response
