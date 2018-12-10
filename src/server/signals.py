from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from sirs.settings import MASTER, REPLICAS
from server.models import File, User, Role


def valid_replication(kwargs):
    valid_model = kwargs['sender'] in [File, User, Role]
    valid_database = kwargs['using'] == MASTER
    return valid_model and valid_database


@receiver(post_save, dispatch_uid="save_uid")
def replicate_save(**kwargs):
    if not valid_replication(kwargs):
        return

    for replica in REPLICAS:
        kwargs['instance'].save(using=replica)


# The replicas are deleted before the main version because the primary key is lost after the object be deleted
@receiver(pre_delete, dispatch_uid="delete_uid")
def replicate_delete(**kwargs):
    if not valid_replication(kwargs):
        return

    for replica in REPLICAS:
        inst_id = kwargs['instance'].id
        rep_inst = kwargs['sender'].objects.using(replica).get(pk=inst_id)
        rep_inst.delete(using=replica)
