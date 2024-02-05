from django.db import models
from django.urls import reverse
from django.utils import timezone


from mentions.models.mixins import MentionableMixin


# Create your models here.


class Reaction(MentionableMixin, models.Model):
    like = 0
    reply = 1
    repost = 2
    reaction_choices = [(like, "Like"), (reply, "Reply"), (repost, "Repost")]

    id = models.AutoField(primary_key=True, unique=True, verbose_name="Post ID")
    create_date = models.DateTimeField(blank=True, null=True, verbose_name="Created")
    reaction_type = models.IntegerField(
        choices=reaction_choices, default=like, verbose_name="Reaction type"
    )
    react_to_url = models.CharField(max_length=1024, verbose_name="Reacting to URL")

    def generate_reaction_html(self):
        bridgy_links = f'<a class="u-like-of" href="{self.react_to_url}"></a><a class="u-bridgy-fed" href="https://fed.brid.gy/" hidden="from-humans"></a>'
        return bridgy_links

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.create_date = timezone.now().replace(microsecond=0)
        super().save(*args, **kwargs)

    def get_content_html(self) -> str:
        return self.generate_reaction_html()

    def get_absolute_url(self) -> str:
        return reverse("reaction_detail", kwargs={"id": str(self.id)})

    def __str__(self):
        return f"{self.get_reaction_type_display()}: {self.react_to_url}"

    class Meta:
        db_table = "cp_reactions"
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"
        ordering = ["-create_date"]
