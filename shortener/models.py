from django.db import models
from django.contrib.auth.models import User
from hashids import Hashids

hashids = Hashids(salt="url_shortener_secret_salt_123", min_length=5)

class ShortenedURL(models.fields.Field):
    pass # Fix for pylance

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2000)
    short_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='urls')
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.short_id:
            self.short_id = hashids.encode(self.id)
            super().save(update_fields=['short_id'])

    def __str__(self):
        return f"{self.short_id} -> {self.original_url[:50]}"
