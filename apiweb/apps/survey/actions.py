from datetime import datetime

import xlwt
from django.http import HttpResponse

from ..alumni.models import Alumnus
from .models import JobAfterLeaving


def save_all_jobs_to_xls(request, queryset=None):
    xls = xlwt.Workbook(encoding="utf8")
    sheet = xls.add_sheet("API Jobs Export")

    alumnus_attributes = [
        "academic_title",
        "initials",
        "first_name",
        "nickname",
        "middle_names",
        "prefix",
        "last_name",
        "gender",
        "survey_info_updated",
    ]

    attributes = [
        "which_position",
        "sector",
        "company_name",
        "position_name",
        "is_inside_academia",
        "location_job",
        "start_date",
        "stop_date",
    ]

    # Define custom styles.
    borders = xlwt.easyxf("borders: top thin, right thin, bottom  thin, left thin;")
    boldborders = xlwt.easyxf(
        "font: bold on; borders: top thin, right thin, bottom  thin, left thin;"
    )

    row = 0  # Create header.
    for col, attr in enumerate(alumnus_attributes):
        sheet.write(row, col, attr, style=boldborders)
    for col, attr in enumerate(attributes):
        sheet.write(row, col + len(alumnus_attributes), attr, style=boldborders)

    if queryset:
        jobs = queryset
    else:  # used to export all theses to Excel
        jobs = JobAfterLeaving.objects.all()
        jobs = jobs.order_by("alumnus__last_name")

    for row, job in enumerate(jobs):
        for col, attr in enumerate(alumnus_attributes):
            try:
                if (attr == "last_name") or (attr == "first_name"):
                    value = str(getattr(job.alumnus, attr, ""))
                else:
                    value = str(getattr(job.alumnus, attr, "")).encode(
                        "ascii", "ignore"
                    )
            except UnicodeEncodeError:
                value = "UnicodeEncodeError"

            # The formatter cannot handle bytes type classes (unicode is not evaluated in bytes).
            # Change to unicode if necessary
            if type(value) is bytes:
                value = value.decode("unicode_escape")

            # Do some cleanups
            if value == "None":
                value = ""

            if attr == "gender":
                if not value == "":
                    value = Alumnus.GENDER_CHOICES[int(value) - 1][1]

            if attr == "survey_info_updated":
                if not value == "":
                    value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f").strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

            sheet.write(row + 1, col, value, style=borders)

        for col, attr in enumerate(attributes):
            try:
                value = str(getattr(job, attr, "")).encode("ascii", "ignore")

            except UnicodeEncodeError:
                value = "UnicodeEncodeError"

            # The formatter cannot handle bytes type classes (unicode is not evaluated in bytes).
            # Change to unicode if necessary
            if type(value) is bytes:
                value = value.decode("unicode_escape")

            if attr == "which_position":
                if not value == "":
                    value = JobAfterLeaving.WHICH_POSITION_CHOICES[int(value)][1]

            if attr == "is_inside_academia":
                if not value == "":
                    value = JobAfterLeaving.YES_OR_NO[int(value) - 1][1]

            # Do some cleanups
            if value == "None":
                value = ""

            sheet.write(row + 1, col + len(alumnus_attributes), value, style=borders)

    # Return a response that allows to download the xls-file.
    now = datetime.now().strftime("%s" % ("%d_%b_%Y"))
    filename = "API_Jobs_Export_{0}.xls".format(now)

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
    xls.save(response)
    return response
