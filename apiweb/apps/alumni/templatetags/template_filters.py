from django import template
from urlobject import URLObject
from django.contrib.staticfiles.templatetags.staticfiles import static
from ..models import Alumnus

register = template.Library()

@register.simple_tag(name='filter_objects', takes_context=True)
def filter_objects(context, filter_type, value):
    '''
    Takes two string parameters: filtertype is the category that will be
    filtered (e.g. "store_filter"), value is the subselection that is wanted
    (e.g. store ID).
    '''
    url = URLObject(context.request.get_full_path())

    filterdict = url.query.multi_dict

    # Check if filter must be removed (if value = 'None')
    if value == 'None':
        new_url = url.del_query_param(filter_type)
        return new_url

    # Allow only one choice each time for gender
    if filter_type == 'gender':
        new_url = url.set_query_param(filter_type, value)
        return new_url

    value = str(value)
    # If you add a new filter you start at page 1 again
    # url = url.del_query_param('page')

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
    if filter_type == 'sort':
        new_url = url.set_query_param(filter_type, value)

    return new_url

@register.simple_tag(name='check_dropdown', takes_context=True)
def check_dropdown(context, filter_type, value):
    '''
    Checks for each filter type and value if the dropdown checkbox should
    be marked or not (whether it is on or off)
    '''
    url = URLObject(context.request.get_full_path())

    # Get dictionary of all the filter types and values in the url
    filters = url.query.multi_dict

    # Check if the to be checked value is in the dictionary
    if filter_type in filters.keys():
        if str(value) in filters[filter_type]:
            return static('img/checkbox-on.png')  # "http://2.bp.blogspot.com/-n1da2kDa_ZY/UXeCtSd5KJI/AAAAAAAAAMw/0ktttvBNCWU/s1600/check_box.png"

    # If it is not in the dictionary return the empty checkbox
    return static('img/checkbox-off.png') # "http://www.clipartbest.com/cliparts/LiK/rrX/LiKrrXy4T.png"

@register.simple_tag(name='get_defence_years')
def get_defence_years():

	options = [('1960 - 1969', 1960, 1969),
			   ('1970 - 1979', 1970, 1979),
			   ('1980 - 1989', 1980, 1989),
			   ('1990 - 1999', 1990, 1999),
			   ('2000 - 2009', 2000, 2009),
			   ('2010 - 2019', 2010, 2019)]

	return options

@register.simple_tag(name='get_genders')
def get_genders():
	return Alumnus.GENDER_CHOICES
