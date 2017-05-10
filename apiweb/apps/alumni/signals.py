from __future__ import unicode_literals, absolute_import, division

from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Alumnus

# Note that the signals are loaded in the ready function in apps.py

@receiver(signals.post_delete, sender=Alumnus)
def delete_user_when_alumnus_is_deleted(sender, instance=None, **kwargs):
    """ When Alumnus instance is deleted, the post_delete signal is sent.
        Here we receive the post_delete signal to also remove the related
        User instance. Note that this does not ask for confirmation in
        the Admin upon deleting the Alumnus instance. """
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()

@receiver(signals.post_save, sender=Alumnus)
def update_user_email_when_alumnus_email_changes(sender, instance=None, **kwargs):
    """ When Alumnus instance is saved, the post_save signal is sent.
        Here we receive the post_save signal to make sure that updating the
        Alumnus first_name, last_name, and/or email address results in an update
        of the corresponding User fields too. """

    # TODO: when the User email is changed, the Alumnus email field is not updated.
    # We cannot receive a signal from sender=User because then saving will result
    # in infinite recursion. Alternatively, the first_name, last_name and email
    # could be removed from the Alumnus class, and the fields from the User could be
    # used instead
    instance.user.first_name = instance.first_name
    instance.user.last_name = instance.last_name

    # User.email may not be NULL, but Alumnus.user may be NULL. Only update if the Alumnus has non-NULL email.
    if instance.email:
        instance.user.email = instance.email

    instance.user.save()
