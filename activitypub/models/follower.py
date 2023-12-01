from django.db import models


# Create your models here.


class Follower(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name="Follower ID")
    actor_id = models.URLField(unique=True)
    accepted = models.BooleanField(default=True)
    raw_json = models.JSONField()
    preferred_username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    inbox_url = models.URLField()
    outbox_url = models.URLField()

    def __str__(self):
        return self.preferred_username

    class Meta:
        db_table = "activitypub_followers"
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        ordering = ["id"]
