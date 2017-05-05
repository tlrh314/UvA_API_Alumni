#! /usr/bin/env python

from __future__ import unicode_literals, absolute_import, division

from ..people.models import Person
import re


def tooltips():
    tooltips = {}
    for person in Person.objects.filter(show_person=True).filter(
            office__isnull=False):
        regex = re.search('(?P<office>\d{3}[a-z]?)', person.office)
        if not regex:
            continue
        office = regex.group('office')
        tooltips.setdefault(office, []).append(
            '<li>{}</li>'.format(person.full_name))
    tips = []
    for key, tooltip in tooltips.items():
        tips.append('<ul class="hovertip" id="tip_{}">{}</ul>'.format(
            key, "\n".join(tooltip)))
    return tips


## Stuff below is old, and was used to create the HTML for the map
## Note that this is an old map, before the second office revamp
#class Group(object):
#    pass
#
#
#def print_svg(svg):
#    lines = []
#    tooltips = []
#    isopen = True if len(svg.children) > 0 else False
#    for obj in svg.objects:
#        if isinstance(obj, Group):
#            l, t = print_svg(obj)
#            lines.extend(l)
#            tooltips.extend(t)
#            line = '  ' * svg.indent
#            line += "</svg:g>"
#            lines.append(line)
#        elif isinstance(obj, dict):
#            key = obj.keys()[0]
#            if key == 'group':
#                key = 'g'
#            value = obj.values()[0]
#            line = '  ' * svg.indent
#            line += "<svg:%s" % key
#            for k, v in value.items():
#                if k == 'text':
#                    pass
#                line += ' %s="%s"' % (k, v)
#                if key == 'g' and k == 'id' and not 'tag' in v:
#                    persons = Person.objects.filter(show_person=True).filter(
#                        office__contains=v).order_by('last_name')
#                    if persons.count():
#                        line += ' class="hover"'
#                        tooltip = '<div class="hovertip" ' + \
#                                  'id="tip_%s">\n<ul>' % v
#                        tooltip += '\n'.join([
#                    '<li>%s</li>' % person.full_name for person in persons])
#                        tooltip += '</ul>\n</div>'
#                        tooltips.append(tooltip)
#                    line += (' onmouseover="highlightnames(%s);" '
#                             ' onmouseout="highlightnames(-%s);"' %
#                             (v, v))
#            #lines.append(line)
#            if key == 'text':
#                line += ">%s</svg:text>" % value['text']
#            if key != 'g':
#                line += " />"
#            else:
#                line += ">"
#            lines.append(line)
#    return lines, tooltips
#
#
#def parse_line(string):
#    words = string.split()
#    value = ""
#    params = {}
#    for word in words:
#        if '=' in word:
#            key, value = word.split('=')
#            params[key] = value
#        else:
#            value += " " + word
#            params[key] = value
#    return params
#
#
#def parse(apimap):
#    previndent = -1
#    group = None
#    for i, line in enumerate(apimap.split('\n')):
#        lline = line.rstrip()
#        if len(lline) == 0:
#            continue
#        llline = lline.lstrip()
#        indent = len(lline) - len(llline)
#        if indent > previndent:
#            parent = group
#            group = Group()
#            if parent is not None:
#                parent.children.append(group)
#                parent.objects.append(group)
#            group.parent = parent
#            group.objects = []
#            group.children = []
#            previndent = indent
#        elif indent < previndent:
#            while indent < previndent:
#                #group.parent.objects.append(group)
#                group = group.parent
#                previndent -= 1
#        try:
#            obj, string = llline.split(None, 1)
#            params = parse_line(string)
#        except ValueError:
#            obj = llline
#            params = {}
#        group.indent = indent
#        group.objects.append({obj: params})
#    while group.parent:  # reset to main parent
#        group = group.parent
#    return group
#
#
#def draw():
#    return """\
#group fill=#fff stroke=black
# path d=M0 448 L0 0 L312 0
# group id=117
#  rect x=270 y=0 width=115 height=50 stroke=none
#  path d=M385 50 L270 50 stroke-dasharray=4,4
#  path d=M385 50 L385 0 L270 0 L270 50
#  group id=tag117 stroke=#ff0000
#   text x=255 y=17 fill=red stroke=none style=font-family: Helvetica, Arial, \
# sans-serif; font-size: 110%; text=117
#  group id=tag_commonroom stroke=#ff0000
#   text x=300 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
# sans-serif; font-size: 110%; text=Common room
# group id=128
#  path d=M0 50 L0 0 L140 0 L140 50
#  path d=M0 50 L140 50 M60 0 L60 50 stroke-dasharray=4,4
#  path d=M0 70 L50 70 L50 115 stroke-dasharray=4,4
#  path d=M0 70 L0 115 L50 115
#  group id=tag_128 stroke=red
#   text x=15 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=128
#   text x=77 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=128
#   text x=15 y=90 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=128
# group id=126
#  rect x=140 y=0 width=35 height=50
#  group id=tag_126 stroke=red
#   text x=150 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=126
# group id=124
#  rect x=175 y=0 width=70 height=50
#  group id=tag_124 stroke=red
#   text x=200 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=124
# group id=121
#  rect x=245 y=0 width=35 height=50
#  group id=tag_121 stroke=red
#   text x=255 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=121
# group id=114
#  rect x=420 y=0 width=35 height=50
#  group id=tag_114 stroke=red
#   text x=425 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=114
# group id=112
#  rect x=455 y=0 width=35 height=50
#  group id=tag_112 stroke=red
#   text x=460 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=112
# group id=110
#  rect x=490 y=0 width=35 height=50
#  group id=tag_110 stroke=red
#   text x=495 y=30 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=110
# group
#  path d=M525 0 L720 0 M525 50 L720 50 stroke-dasharray=4,4
#  path d=M525 0 L525 50 M720 0 L720 50
# group
#  rect x=720 y=0 width=35 height=50
# group id=125
#  rect x=140 y=70 width=35 height=50
#  group id=tag_125 stroke=red
#   text x=150 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=125
# group id=123
#  rect x=175 y=70 width=35 height=50
#  group id=tag_123 stroke=red
#   text x=185 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=123
# group id=122
#  rect x=210 y=70 width=35 height=50
#  group id=tag_110 stroke=red
#   text x=220 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=122
# group id=120
#  rect x=245 y=70 width=35 height=50
#  group id=tag_120 stroke=red
#   text x=255 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=120
# group id=119
#  rect x=280 y=70 width=35 height=50
#  group id=tag_119 stroke=red
#   text x=290 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=119
# group id=118
#  rect x=315 y=70 width=35 height=50
#  group id=tag_118 stroke=red
#   text x=325 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=118
# group id=116
#  rect x=350 y=70 width=35 height=50
#  group id=tag_116 stroke=red
#   text x=360 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=116
# group id=115
#  rect x=385 y=70 width=35 height=50
#  group id=tag_115 stroke=red
#   text x=395 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=115
# group id=113
#  rect x=420 y=70 width=35 height=50
#  group id=tag_113 stroke=red
#   text x=430 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=113
# group id=111
#  rect x=455 y=70 width=35 height=50
#  group id=tag_111 stroke=red
#   text x=465 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=111
# group id=109
#  rect x=490 y=70 width=35 height=50
#  group id=tag_109 stroke=red
#   text x=500 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=109
# group id=108
#  rect x=525 y=70 width=35 height=50
#  group id=tag_108 stroke=red
#   text x=535 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=108
# group id=107
#  rect x=560 y=70 width=35 height=50
#  group id=tag_107 stroke=red
#   text x=570 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=107
# group id=106
#  rect x=595 y=70 width=35 height=50
#  group id=tag_106 stroke=red
#   text x=605 y=100 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=106
# group id=105
#  path d=M630 70 L700 70 L700 140 stroke-dasharray=4,4
#  path d=M630 70 L630 140 L700 140
#  group id=tag_105 stroke=red
#   text x=660 y=110 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=105
# group id=172
#  path d=M720 90 L790 90 L790 205 L720 205
#  path d=M720 205 L720 90 stroke-dasharray=4,4
#  path d=M720 225 L790 225 L790 305 L720 305
#  path d=M720 305 L720 225 stroke-dasharray=4,4
#  group id=tag_172 stroke=red
#   text x=740 y=150 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=172
#   text x=740 y=270 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=172
# group
#  path d=M720 320 L790 320 L790 485 L720 485
#  path d=M720 320 L720 485 stroke-dasharray=4,4
#  group id=tag_IBED stroke=red
#   text x=740 y=400 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group id=171
#  rect x=650 y=140 width=50 height=50
#  group id=tag_171 stroke=red
#   text x=665 y=170 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=171
# group id=170
#  rect x=650 y=190 width=50 height=50
#  group id=tag_170 stroke=red
#   text x=665 y=220 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=170
# group id=169
#  rect x=650 y=240 width=50 height=50
#  group id=tag_172 stroke=red
#   text x=665 y=270 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=169
# group id=168
#  rect x=650 y=290 width=50 height=50
#  group id=tag_168 stroke=red
#   text x=665 y=320 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group id=167
#  rect x=650 y=340 width=50 height=50
#  group id=tag_167 stroke=red
#   text x=665 y=370 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group id=166
#  rect x=650 y=390 width=50 height=50
#  group id=tag_166 stroke=red
#   text x=665 y=420 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group id=165
#  path d=M700 440 L630 440 L630 510
#  path d=M700 440 L700 510 L630 510 stroke-dasharray=4,4
#  group id=tag_165 stroke=red
#   text x=660 y=490 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=165
# group id=127
#  path d=M140 70 L70 70 L70 140 stroke-dasharray=4,4
#  path d=M140 70 L140 140 L70 140
#  group id=tag_127 stroke=red
#   text x=95 y=110 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=127
# group id=129
#  rect x=0 y=115 width=50 height=50
#  group id=tag_129 stroke=red
#   text x=15 y=145 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=129
# group id=131
#  rect x=0 y=165 width=50 height=50
#  group id=tag_13 stroke=red
#   text x=15 y=195 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=131
# group id=133
#  rect x=0 y=215 width=50 height=50
#  group id=tag_133 stroke=red
#   text x=15 y=245 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=133
# group
#  rect x=0 y=265 width=50 height=50
#  group id=tag_p stroke=red
#   text x=15 y=295 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group
#  rect x=0 y=315 width=50 height=50
#  group id=tag_q stroke=red
#   text x=15 y=345 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group
#  rect x=0 y=365 width=50 height=50
#  group id=tag_w stroke=red
#   text x=15 y=395 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group
#  rect x=0 y=415 width=50 height=50
#  group id=tag_v stroke=red
#   text x=15 y=445 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group id=130
#  rect x=70 y=140 width=50 height=50
#  group id=tag_130 stroke=red
#   text x=85 y=170 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=130
# group id=132
#  rect x=70 y=190 width=50 height=50
#  group id=tag_132 stroke=red
#   text x=85 y=220 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=132
# group id=134
#  rect x=70 y=240 width=50 height=50
#  group id=tag_134 stroke=red
#   text x=85 y=270 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=134
# group
#  rect x=70 y=290 width=50 height=50
#  group id=tag_z stroke=red
#   text x=85 y=320 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group
#  rect x=70 y=340 width=50 height=50
#  group id=tag_y stroke=red
#   text x=85 y=370 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group
#  rect x=70 y=390 width=50 height=50
#  group id=tag_x stroke=red
#   text x=85 y=420 fill=red stroke=none style=font-family: Helvetica, Arial, \
#sans-serif; font-size: 110%; text=
# group
#  path d=M70 440 L70 510 L140 510 stroke-dasharray=4,4
#  path d=M70 440 L140 440 L140 510
# group
#  rect x=140 y=460 width=35 height=50
# group
#  rect x=175 y=460 width=35 height=50
# group
#  rect x=210 y=460 width=35 height=50
# group
#  rect x=245 y=460 width=35 height=50
# group
#  rect x=280 y=460 width=35 height=50
# group
#  rect x=315 y=460 width=35 height=50
# group
#  rect x=350 y=460 width=35 height=50
# group
#  rect x=385 y=460 width=35 height=50
# group
#  rect x=420 y=460 width=35 height=50
# group
#  rect x=455 y=460 width=35 height=50
# group
#  rect x=490 y=460 width=35 height=50
# group
#  rect x=525 y=460 width=35 height=50
# group
#  rect x=560 y=460 width=35 height=50
# group
#  rect x=595 y=460 width=35 height=50
#  """
#
#
#def create():
#    apimap = draw()
#    svg = parse(apimap)
#    return print_svg(svg)
#
#if __name__ == "__main__":
#    print "".join(create()[0])
