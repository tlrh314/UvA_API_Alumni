from __future__ import absolute_import, division, unicode_literals

import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

try:
    inttypes = (int, long)
except NameError:
    inttypes = (int,)


register = template.Library()


@register.filter
def truncchar(value, arg):
    """
    Truncate after a certain number of characters.
    Source: http://www.djangosnippets.org/snippets/194/
    Notes
    -----
    Super stripped down filter to truncate after a certain number of letters.
    Example
    -------
    {{ long_blurb|truncchar:20 }}
    The above will display 20 characters of the long blurb followed by "..."
    """

    if len(value) < arg:
        return value
    else:
        return value[:arg] + "..."


@register.filter
def re_sub(string, args):
    """
    Provide a full regular expression replace on strings in templates
    Usage:
    {{ my_variable|re_sub:"/(foo|bar)/baaz/" }}
    """
    old = args.split(args[0])[1]
    new = args.split(args[0])[2]
    return re.sub(old, new, string)


@register.filter
def replace(string, args):
    """
    Provide a standard Python string replace in templates
    Usage:
    {{ my_variable|replace:"/foo/bar/" }}
    """
    old = args.split(args[0])[1]
    new = args.split(args[0])[2]
    return string.replace(old, new)


@register.filter
def re_label(string):
    old = "/"
    new = "/ </br>"
    return string.replace(old, new)


@register.filter
def hash(d, key):
    try:
        return d[key]
    except (KeyError, TypeError):
        return ""


@register.filter
@template.defaultfilters.stringfilter
def clearemptylines(text):
    """Clear blank lines in resulting HTML"""

    """
    This is just a convenience function,
    to get rid of large amount of whitespace.
    This whitespace is often caused by making a template readable,
    which then causes the resulting HTML to be less readable.
    """

    lines = text.split("\n")
    newlines = []
    for line in lines:
        if line.strip() == "":
            continue
        newlines.append(line)
    return "\n".join(newlines)


#
# @register.filter
# @template.defaultfilters.stringfilter
# def emailize(value):
#    """Turns text with plain email addresses into clickable ones"""
#    return re.sub("(?P<front>^|\s)(?P<email>[^\s]+@[^\s]+)"
#                  "(?P<back>\s|$)",
#                  "\g<front><a href=\"mailto:\g<email>\">"
#                  "\g<email></a>\g<back>", value)
#


@register.filter
def romanize(value):
    """Returns a Roman numeral for an Arabic numeral

    Conversion method taken from diveintopython.org
    """

    if not isinstance(value, inttypes):
        return ""
    if value < 1 or value > 3999:
        return ""
    romanNumeralMap = (
        ("M", 1000),
        ("CM", 900),
        ("D", 500),
        ("CD", 400),
        ("C", 100),
        ("XC", 90),
        ("L", 50),
        ("XL", 40),
        ("X", 10),
        ("IX", 9),
        ("V", 5),
        ("IV", 4),
        ("I", 1),
    )
    result = ""
    for numeral, integer in romanNumeralMap:
        while value >= integer:
            result += numeral
            value -= integer
    return result


@register.filter
def nonbreakable(value, autoescape=None):
    """Replace characters by non-linebreaking equivalenets"""

    # see http://docs.djangoproject.com/en/dev/howto/custom-template-tags/\
    # #filters-and-auto-escaping
    value = conditional_escape(value) if autoescape else value
    # esc = conditional_escape if autoescape else lambda s: s
    characters = " -"
    replacements = ["&nbsp;", "&ndash;"]
    for char, repl in zip(characters, replacements):
        value = value.replace(char, repl)
    return mark_safe(value)


nonbreakable.needs_autoescape = True


@register.filter
def menulist(menu, selected_item="", href_for_select=0):
    """Recursively build up a menu into an unordered list"""

    """
    Build an unordered list that represents a menu.
    The first argument is a list or tuple of three-tuples (or three-lists)
    The first element of the tuple is the visible name of the menu item
    The second tuple element is a link, and be blank ('' or None)
    The third tuple element is either blank, or consists of another
    tuple representing a submenu (and so on, recursively).
    The second argument 'selected_item' is a string that equals the name
    of the currently selected item, and sets that item to the class "selected"
    The third argment is a boolean that sets whether the currently selected
    item is a link, i.e. is clickable.

    E.g.,
    menu = [("item1", '', [("subitem1_1", '/item1/sub1', None),
                           ("subitem1_2", '/item1/sub2', None)]),
            ("item2", '/item2', [("subitem2_1", "/item2/sub1", None)])]

    Calling menu|menulist results in

    <ul>
    <li> item1
    <ul>
    <li> <a href="/item1/sub1">subitem1_1</a> </li>
    <li> <a href="/item1/sub1">subitem1_2</a> </li>
    </ul>
    </li>
    <li> <a href="/item2/sub1">item2</a>
    <ul>
    <li> <a href="/item1/sub1">subitem1_1</a> </li>
    </ul>
    </li>
    </ul>
    """

    selected_item = selected_item.split(",")
    if len(selected_item) == 2:
        href_for_select = int(selected_item[1])
    selected_item = selected_item[0]
    menu_string = "<ul>\n"
    for item in menu:
        label, ref, submenu = item
        if label == selected_item:
            menu_string += '<li class="selected"> '
        else:
            menu_string += "<li> "
        if ref:
            if label != selected_item or href_for_select:
                menu_string += '<a href="{}">'.format(ref)
        menu_string += label
        if ref:
            if label != selected_item or href_for_select is True:
                menu_string += "</a> "
        if isinstance(submenu, (tuple, list)):
            menu_string += "\n" + menulist(submenu, selected_item, href_for_select)
        menu_string += "</li>\n"
    menu_string += "</ul>\n"
    return menu_string


@register.filter
def paginate(page, arg="3,2"):
    """Provide a HTML rendered pagination section, with leading,
    trailing and surrounding page numbers

    First part of the argument is the number of surrounding page numbers,
    the second part the number of leading and trailing page numbers
    at the start and end.

    Other examples at:
    http://code.djangoproject.com/wiki/PaginatorTag
    http://blog.localkinegrinds.com/2007/09/06/digg-style-pagination-in-django/

    """

    args = [int(val) for val in arg.split(",")]
    if len(args) > 0:
        surrounding = args[0]
        leading = trailing = 2
    if len(args) > 1:
        leading = trailing = args[1]
    paginator = page.paginator
    if paginator.num_pages == 1 or 0 in [surrounding, leading, trailing]:
        return ""
    current = page.number
    firstpage, lastpage = 1, paginator.num_pages
    start = set(range(firstpage, leading + 1))
    end = set(range(lastpage + 1 - trailing, lastpage + 1))
    surround = set(
        range(
            max(1, current - surrounding), min(lastpage + 1, current + surrounding + 1)
        )
    )
    ellipses = True, True
    if start.intersection(surround) or max(start) + 1 == min(surround):
        start = start.union(surround)
        surround = set()
        ellipses = False, True
    elif end.intersection(surround) or min(end) - 1 == max(surround):
        end = end.union(surround)
        surround = set()
        ellipses = True, False
    if start.intersection(end) or max(start) + 1 == min(end):
        start = start.union(end)
        end = set()
        surround = ()
        ellipses = False, False
    pagenumbers = []
    if current > 1:
        pagenumbers.append('<a href="?page={}">previous</a>'.format(current - 1))
    for num in sorted(start):
        if num == current:
            pagenumbers.append("{}".format(num))
        else:
            pagenumbers.append('<a href="?page={}">{}</a>'.format(num, num))
    if ellipses[0]:
        pagenumbers.append("...")
    for num in sorted(surround):
        if num == current:
            pagenumbers.append("{}".format(num))
        else:
            pagenumbers.append('<a href="?page={}">{}</a>'.format(num, num))
    if ellipses[1]:
        pagenumbers.append("...")
    for num in sorted(end):
        if num == current:
            pagenumbers.append("{}".format(num))
        else:
            pagenumbers.append('<a href="?page={}">{}</a>'.format(num, num))
    if current < lastpage:
        pagenumbers.append('<a href="?page={}">next</a>'.format(current + 1))
    return mark_safe("|".join(pagenumbers))


@register.filter
def mod(value, arg):
    if value % arg == 0:
        return True
    else:
        return False
