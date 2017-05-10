from django.apps import AppConfig


class AlumniConfig(AppConfig):
    name = "apiweb.apps.alumni"

    # https://docs.djangoproject.com/en/1.11/topics/signals/#connecting-receiver-functions
    def ready(self):
        from apiweb.apps.alumni.signals import delete_user_when_alumnus_is_deleted
        from apiweb.apps.alumni.signals import update_user_email_when_alumnus_email_changes
