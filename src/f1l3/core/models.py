import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.utils import generate_random_sequence


def random_filename(_, filename: str) -> str:
    if not filename:
        raise ValueError("invalid filename")
    ext = os.path.splitext(filename)[1]
    ext = ext or ".bin"
    return str(uuid.uuid4()) + ext


class UploadedFile(models.Model):
    file = models.FileField(upload_to=random_filename)
    alias = models.TextField(null=True, blank=True, unique=True)

    def remove(self):
        self.file.delete()
        self.delete()


@receiver(post_save, sender=UploadedFile)
def update_alias(sender, instance, **kwargs):
    if getattr(instance, "alias", None) is not None:
        return
    current_length = 3
    cnt = sender.objects.count()
    clash_rate = cnt / 10**current_length
    while clash_rate > 0.3:
        current_length += 1
        clash_rate = cnt / 10**current_length
    alias = None
    while alias is None or sender.objects.filter(alias=alias).exists():
        alias = generate_random_sequence(current_length)
    instance.alias = alias
    instance.save()
