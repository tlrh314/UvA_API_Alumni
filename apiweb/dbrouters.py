# Turn off pylint warning us for sticking to the function definition:
# pylint: disable=unused-argument


class DefaultRouter(object):
    """A router to control the database operations on all models,
    except the API WIKI"""

    def db_for_read(self, model, **hints):
        return "default"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label != "wiki" and obj2._meta.app_label != "wiki":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True


class WikiRouter(object):
    """A router to control all database operations on models in the API WIKI"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "wiki":
            return "wiki"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "wiki":
            return "wiki"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "wiki" or obj2._meta.app_label == "wiki":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "wiki":
            return app_label == "wiki"
        elif app_label == "wiki":
            return False
        return None
