from django import template

from ...alumni.models import Alumnus, PreviousPosition, PositionType

register = template.Library()

# @register.filter
# def author_name(post):
#     alumnus = Alumnus.objects.filter(user=post.author)
#     if alumnus:
#         return alumnus.full_name
#     else:
#         return post.author
#
#

@register.simple_tag(name="get_postdoc_year")
def get_postdoc_year(alumnus):
    # TODO: which position type to include as staff?
    postdoc_set = alumnus.positions.filter(type__name__in=["Postdoc", ])

    if not postdoc_set:
        return ""

    date_stop = postdoc_set[0].date_stop
    for pos in postdoc_set:
        if not pos.date_stop:
            continue
        if pos.date_stop > date_stop:
            date_stop = pos.date_stop

    if not date_stop:
        return "Current"
    else:
        return date_stop.strftime("%Y")


@register.simple_tag(name="get_staff_year")
def get_staff_year(alumnus):
    # TODO: which position type to include as staff?
    staff_set = alumnus.positions.filter(type__name__in=[
        "Research Staff", "Adjunct Staff", "Faculty Staff", "Teacher",
        "Emeritus", ])

    if not staff_set:
        return ""

    date_stop = staff_set[0].date_stop
    for pos in staff_set:
        if not pos.date_stop:
            continue
        if pos.date_stop > date_stop:
            date_stop = pos.date_stop

    if not date_stop:
        return "Current"
    else:
        return date_stop.strftime("%Y")


@register.simple_tag(name="get_obp_year")
def get_obp_year(alumnus):
    # TODO: which position type to include as OBP ?
    obp_set = alumnus.positions.filter(type__name__in=[
        "Instrumentation", "Institute Manager", "Outreach", "OBP",
        "Software Developer", "Nova" ])

    if not obp_set:
        return ""

    date_stop = obp_set[0].date_stop
    for pos in obp_set:
        if not pos.date_stop:
            continue
        if pos.date_stop > date_stop:
            date_stop = pos.date_stop

    if not date_stop:
        return "Current"
    else:
        return date_stop.strftime("%Y")

