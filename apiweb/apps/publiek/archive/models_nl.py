from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Activity(models.Model):
    """Represents an activity for a person to do."""

    nr = models.PositiveSmallIntegerField(_('number of activity'),
                                          primary_key=True)
    is_in_block1 = models.BooleanField(_('is activity part of block1?'),
                                       default=False)
    is_in_block2 = models.BooleanField(_('is activity part of block2?'),
                                       default=False)
    is_in_block3 = models.BooleanField(_('is activity part of block3?'),
                                       default=False)
    name = models.CharField(_('naam'), max_length=40)
    max_people = models.PositiveSmallIntegerField(
        _('maximum of people allowed for this activity'))

    class Meta:
        verbose_name_plural = _('activities')

    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class Starnight(models.Model):
    """Represents a day when the public visit the apo.
       Only one date can have is_registrable being True."""

    date = models.DateField(_('starnight datum'), unique=True)
    max_people = models.PositiveSmallIntegerField(
        _('maxium of people for this starnight'))
    is_registrable = models.BooleanField(
        _('is date open for registration?'), default=False,
        help_text="If True, this night is now open for registration")
#
# Nu was blocks verplicht, mischien beter om dit niet veplicht te maken,
# indien er een starnight komt zonder blok, gewoon met 1 specifiek programma
#
#    blocks = models.ManyToManyField(Block, related_name='blocks', blank=True)
#
#    def is_full(self, datum):
#        """Determine whether we have reached the complete registration limit.
#
#         This does *not* automatically close the registration, that is,
#         it does not set `is_registrable` to False.
#
#         """
#         # Get all the people for tonight
#         participants = Participant.objects.filter(self.date = datum)
#         blocks = self.blocks.all()
#         for block in blocks:
#             # Get all the activities for this block
#             activities = block.activities.all()
#             for activity in activities:
#                 # Find all the participants for this activity
#                 participants = Participant.objects.filter(
#                     activity__pk=activity.pk)
#                 if participants.count() < acitivity.maxamount:
#                     # Still space for people in this activity
#                     return False
#         return True

    def __str__(self):
        return str(self.date)


@python_2_unicode_compatible
class StarnightApplicant(models.Model):
    """Represents someone who wants to see the stars."""

    NL_CHOICES = (
        (0, 'Nee'),
        (1, 'Ja'),
    )

    NR_CHOICES = (
        (1, ' 1'), (2, ' 2'), (3, ' 3'), (4, ' 4'), (5, ' 5'),
        (6, ' 6'), (7, ' 7'), (8, ' 8'), (9, ' 9'), (10, '10'),
    )

#
# Do not know when you can use this.
#    date = models.ForeignKey(Starnight, related_name='datum',
#                             limit_choices_to={'is_registrable': True})
#

    date = models.ForeignKey(Starnight, related_name='datum')
    name = models.CharField(_('naam'), max_length=40)
    address = models.CharField(_('adres'), max_length=40)
    zipcode = models.CharField(_('postcode'), max_length=40)
    city = models.CharField(_('plaats'), max_length=40)
    email = models.EmailField(_('e-mail'))
    newsletter = models.PositiveSmallIntegerField(_('nieuwsbrief'),
                                                  choices=NL_CHOICES)
    number = models.PositiveSmallIntegerField(_('aantal mensen'),
                                              choices=NR_CHOICES, default=1)

    slot1 = models.ForeignKey(Activity, related_name='slot1', default=0)
    slot2 = models.ForeignKey(Activity, related_name='slot2', default=0)
    slot3 = models.ForeignKey(Activity, related_name='slot3', default=0)

    def __str__(self):
        return str(self.name)
