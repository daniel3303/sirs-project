from sirs.settings import MASTER


class Router:
    def db_for_read(self, model, **hints):
        return MASTER

    def db_for_write(self, model, **hints):
        return MASTER

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True