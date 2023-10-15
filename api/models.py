import random

import json
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    full_url = models.URLField(unique=True)
    short_url = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=True
    )
    requests_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_date',)

    def save(self, *args, **kwargs):

        if not self.short_url:
            while True:
                self.short_url = ''.join(
                    random.choices(
                        settings.CHARACTERS,
                        k=settings.TOKEN_LENGTH
                    )
                )
                if not Token.objects.filter(
                        short_url=self.short_url
                ).exists():
                    break
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.short_url} -> {self.full_url}'


class UserSavedLinks(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    link_pairs = models.TextField(default="[]")

    def set_link_pairs(self, pairs_list):
        self.link_pairs = json.dumps(pairs_list)

    def get_link_pairs(self):
        return json.loads(self.link_pairs)