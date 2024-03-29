from django import template
from django.templatetags.static import static
from django.utils.html import conditional_escape
from django.utils.http import urlquote
from django.utils.safestring import mark_safe
from urlobject import URLObject

from ...research.models import Thesis

register = template.Library()


@register.simple_tag(name="filter_objects", takes_context=True)
def filter_objects(context, filter_type, value):
    """Takes two string parameters: filtertype is the category that will be
    filtered (e.g. "year"), value is the subselection that is wanted
    (e.g. 2010-2019)."""

    url = URLObject(context.request.get_full_path())

    filterdict = url.query.multi_dict

    # Check if filter must be removed (if value = "None")
    if value == "None":
        new_url = url.del_query_param(filter_type)
        return new_url

    value = str(value)

    # If you add a new filter you start at page 1 again
    # url = url.del_query_param("page")

    # Check if same filter is clicked again -> uncheck
    if filter_type in filterdict and str(value) in filterdict[filter_type]:
        values = filterdict[filter_type]
        values.remove(value)
        new_url = url.del_query_param(filter_type)
        if values:
            for v in values:
                new_url = new_url.add_query_param(filter_type, v)
        return new_url

    # Add new filter
    new_url = url.add_query_param(filter_type, value)

    # Check if the filter is already in the url string and replace
    if filter_type == "sort":
        new_url = url.set_query_param(filter_type, value)

    return new_url


@register.simple_tag(name="check_dropdown", takes_context=True)
def check_dropdown(context, filter_type, value):
    """Checks for each filter type and value if the dropdown checkbox should
    be marked or not (whether it is on or off)"""

    url = URLObject(context.request.get_full_path())

    # Get dictionary of all the filter types and values in the url
    filters = url.query.multi_dict

    # Check if the to be checked value is in the dictionary
    if filter_type in filters.keys():
        if str(value) in filters[filter_type]:
            return static(
                "img/checkbox-on.png"
            )  # "http://2.bp.blogspot.com/-n1da2kDa_ZY/UXeCtSd5KJI/AAAAAAAAAMw/0ktttvBNCWU/s1600/check_box.png"

    # If it is not in the dictionary return the empty checkbox
    return static(
        "img/checkbox-off.png"
    )  # "http://www.clipartbest.com/cliparts/LiK/rrX/LiKrrXy4T.png"


@register.simple_tag(name="get_active_filters", takes_context=True)
def get_active_filters(context):
    filterzip = []
    active_filters_dict = URLObject(context.request.get_full_path()).query.multi_dict

    for filter_type, filter_values in active_filters_dict.items():
        if filter_type not in ["type", "year", "sort"]:
            continue
        else:
            for filter_value in filter_values:
                filterzip.append((filter_type, filter_value))
    return filterzip


@register.simple_tag(name="get_active_sort", takes_context=True)
def get_active_sort(context):
    active_filters_dict = URLObject(context.request.get_full_path()).query.multi_dict
    order = active_filters_dict.get("sort", None)
    return order[0] if order else None


@register.simple_tag(name="get_defence_years")
def get_defence_years():
    return [
        ("1900 - 1959", 1900, 1959),
        ("1960 - 1969", 1960, 1969),
        ("1970 - 1979", 1970, 1979),
        ("1980 - 1989", 1980, 1989),
        ("1990 - 1999", 1990, 1999),
        ("2000 - 2009", 2000, 2009),
        ("2010 - 2019", 2010, 2019),
    ]


@register.simple_tag(name="get_yearrange")
def get_yearrange(year):
    return {
        "1900": "1900 - 1959",
        "1960": "1960 - 1969",
        "1970": "1970 - 1979",
        "1980": "1980 - 1989",
        "1990": "1990 - 1999",
        "2000": "2000 - 2009",
        "2010": "2010 - 2019",
    }.get(year, "none")


@register.simple_tag(name="get_amount_advisors")
def get_amount_advisors(advisors_list):
    return len(advisors_list)


@register.simple_tag(name="get_thesis_types")
def get_thesis_types():
    return Thesis.THESIS_TYPE


@register.simple_tag(name="get_sorting_options")
def get_sorting_options():
    return [
        ("Author AZ", "author_az"),
        ("Author ZA", "author_za"),
    ]
    # ("Year High-Low", "year_hl"),
    # ("Year Low-High", "year_lh")]


@register.simple_tag(name="set_query", takes_context=True)
def set_query(context, type, value):
    url = URLObject(context.request.get_full_path())
    return url.set_query_param(type, value)


@register.filter(name="capitalize_filter_type")
def capitalize_filter_type(filter_type):
    return filter_type[0].upper() + filter_type[1:]


@register.filter(name="display_thesis_type")
def display_thesis_type(thesis_type):
    return {"phd": "PhD", "msc": "MSc", "bsc": "BSc"}.get(thesis_type, "")


@register.filter(name="display_sort_type")
def display_sort_type(sort_type):
    return {
        "phd": "PhD",
        "msc": "MSc",
        "bsc": "BSc",
        "pd": "Postdoc",
        "staff": "Staff",
        "obp": "Support Staff",
        "alumnus": "Alumnus",
        "author": "Author",
        "thesis": "Thesis",
        "year": "Defence date",
        "title": "Thesis title",
    }.get(sort_type[:-3], "")


@register.filter(name="display_length_result")
def display_length_result(advisors_list):
    return len(advisors_list)


@register.simple_tag(name="filter_content", takes_context=True)
def filter_content(context, filter_type, value):
    """Takes two string parameters: filtertype is the thesis type that will be
    filtered, value is the subselection that is wanted."""

    url = URLObject(context.request.get_full_path())

    if filter_type == "page":
        new_url = url.set_query_param(filter_type, value)
        return new_url

    # If you add a new filter you start at page 1 again
    url = url.del_query_param("page")


@register.simple_tag(name="get_students")
def get_students(alumnus, type):
    theses_supervised = alumnus.students.all().order_by("-date_of_defence")
    return [
        (thesis.alumnus, thesis.date_of_defence)
        for thesis in theses_supervised
        if thesis.type == type
    ]


@register.simple_tag(name="get_thesis_supervisors")
def get_thesis_supervisors(alumnus, thesis_type):
    """
    parameter type: 'msc', 'phd'
    """
    theses = alumnus.theses.filter(type=thesis_type)
    thesis_supervisors = []
    date_of_defence = []
    type_theses = []

    for thesis in theses:
        for supervisor in thesis.advisor.all():
            thesis_supervisors.append(supervisor)
            date_of_defence.append(thesis.date_of_defence)
            type_theses.append(thesis_type)

    # Zip is an iterator so it can only exhaust, but it has no len.
    # Typecast to list such that we can check if the list is empty
    return list(zip(thesis_supervisors, date_of_defence, type_theses))


@register.simple_tag(name="get_supervisors")
def get_supervisors(alumnus):
    """
    Old method, but basically loops over all the theses person has.
    """
    phd_theses = alumnus.theses.filter(type="phd")
    msc_theses = alumnus.theses.filter(type="msc")
    thesis_supervisors = []
    date_of_defence = []
    type_theses = []

    if len(phd_theses) >= 1:
        for phd_thesis in phd_theses:
            for supervisor in phd_thesis.advisor.all():
                thesis_supervisors.append(supervisor)
                date_of_defence.append(phd_thesis.date_of_defence)
                type_theses.append("phd")
    if len(msc_theses) >= 1:
        for msc_thesis in msc_theses:
            for supervisor in msc_thesis.advisor.all():
                thesis_supervisors.append(supervisor)
                date_of_defence.append(msc_thesis.date_of_defence)
                type_theses.append("msc")

    # Zip is an iterator so it can only exhaust, but it has no len.
    # Typecast to list such that we can check if the list is empty
    return list(zip(thesis_supervisors, date_of_defence, type_theses))


@register.filter
@template.defaultfilters.stringfilter
def ads_url(value, autoescape=None):
    """Returns ADS link based on name or on personal library
    See http://doc.adsabs.harvard.edu/abs_doc/help_pages/linking.html"""

    # see http://docs.djangoproject.com/en/dev/howto/custom-template-tags/\
    # #filters-and-auto-escaping
    value = conditional_escape(value) if autoescape else value
    link = ""
    if len(value) == 0:
        return mark_safe(link)
    if value.startswith("libname"):
        link = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?library&" + value
        #      "http://adsabs.harvard.edu/cgi-bin/abs_connect?param1=val1&param2=val2&"
    else:
        link = (
            "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?"
            "db_key=AST&db_key=INST&db_key=PHY&author="
            + urlquote(value)
            + "&nr_to_return=2000&start_nr=1"
        )

    return mark_safe(link)


ads_url.needs_autoescape = True
