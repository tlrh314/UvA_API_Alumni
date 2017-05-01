from __future__ import unicode_literals, absolute_import, division

from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.platypus import CondPageBreak
from reportlab.platypus import Spacer, Image
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import landscape, A4
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from datetime import datetime
import os.path
import re
from ..people.models import Person
from ... import settings


class TelephonelistView(View):

    def foot(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "Page {}".format(doc.page))
        canvas.restoreState()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=phonelist.pdf'

        my_qset = Person.objects.all().filter(
            show_person=True).order_by('last_name')
# A basic document for us to write to 'phonelist.pdf'
        doc = SimpleDocTemplate(response, pagesize=landscape(A4))
        doc.allowSplitting = 1
        doc.showBoundary = 0
        doc.leftMargin = 20.0
        doc.rightMargin = 1.0
        doc.topMargin = 1.0
        doc.bottomMargin = 1.0
# A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
# Our container for 'Flowable' objects
        elements = []
        today = datetime.today()
        my_title = "Telephone List of the Anton Pannekoek Institute for " \
                   "Astronomy --- " + today.strftime("%d-%m-%Y")
        elements.append(Paragraph(my_title, styles['Title']))
        data = []
        data.append(['First Name', 'Last Name', 'Phone', 'E-mail (@uva.nl)',
                     'Office', 'Position', 'Private Address', 'Zipcode', 'City',
                     'Telephone / Mobile'])
        positions = {
            Person.POSITION['DIRECTOR']: "Director",
            Person.POSITION['STAFF']: "Staff",
            Person.POSITION['NOVA']: "Nova",
            Person.POSITION['ADJUNCT']: "Adjunct",
            Person.POSITION['POSTDOC']: "Postdoc",
            Person.POSITION['DEVELOPER']: "S. Dev.",
            Person.POSITION['PHD']: "PhD",
            Person.POSITION['EMERITUS']: "Emeritus",
            Person.POSITION['GUEST']: "Guest",
            Person.POSITION['MASTER']: "MSc",
            Person.POSITION['BACHELOR']: "BSc"}
        for _, person in enumerate(my_qset):
            lastname = person.prefix + ' ' + person.last_name
            phone = re.sub("^\s*020\-525", "", person.work_phone)
            email = re.sub("\@uva\.nl\s*$", "", person.email)
            office = re.sub("^\s*C4\-", "", person.office)
            office = re.sub("^\s*C4\.", "", office)
            position = positions.get(person.position, "Unknown")
            data.append([person.first_name, lastname,
                         phone, email, office, position,
                         person.address, person.zipcode, person.city,
                         person.home_phone + ' / ' + person.mobile])
# First the top row, with all the text centered and in Times-Bold,
# and one line above, one line below.
        ts = [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
              ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
              ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
              # ('FONT', (0, 0), (-1, 0), 'Times-Bold', 10),
              # ('FONT', (0, 1), (-1, -1), 'Times-Roman', 9)]
              ('FONT', (0, 0), (-1, 0), 'Times-Roman', 10),
              ('FONT', (0, 1), (-1, -1), 'Times-Roman', 9)]
# Create the table with the necessary style, and add it to the elements list.
        table = Table(data, style=ts, splitByRow=1, repeatRows=1)
        table.canSplit = 1
        elements.append(table)
# For page break if less than 10 cm's of space is available
        elements.append(CondPageBreak(10*cm))
# Make some space
        elements.append(Spacer(1, 12))
        # API logo
        # {{ STATIC_URL }}internal/images/API_logo_color.jpg
        img = Image(os.path.join(
            settings.BASE_DIR,
            'apps/internal/static/internal/images/API_logo_color.jpg'))
        img.drawHeight = 1.50*inch*img.drawHeight/img.drawWidth
        img.drawWidth = 1.50*inch
# Make an extra table with general information
        data = []
#        data.append(['General', 'Phone', 'Remaining', 'Phone', 'Address', ' '])
#        data.append(['Fire/Injuries', '2222', 'Reception', '8626', \
#'Anton Pannekoek Institute for Astronomy',[img]])
#        data.append(['Emergencies', '112', 'E-mail: receptie-fnwi@uva.nl', \
#' ', 'Visitors: Science Park 904', ' '])
#        data.append(['Facilities', '7575', 'Mail room', '8445', \
#'               1098 XH Amsterdam', ' '])
#        data.append(['E-mail: servicedesk-fc@uva.nl', ' ', 'Storage room', \
#'8446', 'Post:       PO Box 94249', ' '])
#        data.append(['ICT Helpdesk', '2200 ', 'Solar Dome below', '8309', \
#'               1090 GE Amsterdam', ' '])
#        data.append(['E-mail: servicedesk-ic@uva.nl', ' ', 'Solar Dome', \
#'8310', 'Tel: 020-5257491, Fax: 020-5257484', ' '])
#        data.append(['Education Service Centre', '7100 ', 'Stellar Dome', \
#'8311', 'E-mail: secr-astro-science@uva.nl', ' '])
#        data.append(['E-mail: servicedesk-esc@uva.nl ', ' ', \
#'Guest room (C4-130)', '7366', 'E-mail all: institute@list.uva.nl', ' '])
#        data.append([' ', ' ', ' ', ' ', 'WWW: http://www.astro.uva.nl/', ' '])
        data.append(['General', 'Phone', 'Remaining', 'Phone', 'Address', ' '])
        data.append(['Fire/Injuries', '2222', 'Emergencies', '112',
                     'Anton Pannekoek Institute for Astronomy', [img]])
        data.append(['ICT Helpdesk', '2200 ', 'Reception', '8626',
                     'Visitors: Science Park 904', ' '])
        data.append(['E-mail: servicedesk-ic@uva.nl', ' ',
                     'E-mail: receptie-fnwi@uva.nl', ' ',
                     '               1098 XH Amsterdam', ' '])
        data.append(['Facilities', '7575', 'Mail room', '8445',
                     'Post: PO Box 94249', ' '])
        data.append(['E-mail: servicedesk-fc@uva.nl', ' ', 'Storage room',
                     '8446', '               1090 GE Amsterdam', ' '])
        data.append(['Administratief Centrum', '5999', 'Solar Dome below',
                     '8309', 'Tel: 020-5257491, Fax: 020-5257484', ' '])
        data.append(['E-mail: servicedesk-ac@uva.nl', ' ', 'Solar Dome',
                     '8310', 'E-mail: secr-astro-science@uva.nl', ' '])
        data.append(['Education Service Centre', '7100', 'Stellar Dome',
                     '8311', 'E-mail all: institute@list.uva.nl', ' '])
        data.append(['E-mail: servicedesk-esc@uva.nl', ' ', '', ' ',
                     'WWW: http://www.astro.uva.nl/', ' '])
# Create a table style
        ts = [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
              ('ALIGN', (1, 2), (1, 2), 'CENTER'),
              ('ALIGN', (1, 1), (1, -1), 'CENTER'),
              ('ALIGN', (3, 1), (3, -1), 'CENTER'),
              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
              ('BOX', (0, 0), (-1, -1), 1, colors.black),
              ('SPAN', (-1, 1), (-1, -1)),
              ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
              ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
              ('LINEBEFORE', (2, 0), (2, -1), 1, colors.black),
              ('LINEBEFORE', (4, 0), (4, -1), 1, colors.black),
              ('FONT', (0, 0), (-1, 0), 'Times-Bold', 10),
              ('FONT', (0, 1), (-1, -1), 'Times-Roman', 9)]
#             ('FONT', (0, 0), (-1, 0), 'Times-Roman', 10),
#             ('FONT', (0, 1), (-1, -1), 'Times-Roman', 9)]
# Create the table with the necessary style, and add it to the elements list.
        table = Table(data, style=ts)
        table.canSplit = 0
        elements.append(table)
# Create two paragraphs with general telephone numbers
# Two Columns
#        frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width//2-6,
#                       doc.height, id='col1')
#        frame2 = Frame(doc.leftMargin+doc.width//2+6, doc.bottomMargin,
#                       doc.width//2-6, doc.height, id='col2')
#        elements.append(NextPageTemplate('TwoCol'))
#        elements.append(PageBreak())
#        elements.append(Paragraph("Frame two columns,  "*500,styles['Normal']))
#        doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2],
#                              onPage=self.foot), ])
# Start the construction of the pdf
# Write the document to file
        doc.build(elements)
        return response
