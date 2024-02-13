from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify


import utilities


# Create your models here.


class Page(models.Model):
    title = models.CharField(max_length=250, verbose_name="Title")
    description = models.CharField(
        max_length=160, blank=True, null=True, verbose_name="Description"
    )
    text = models.TextField(verbose_name="Markdown text")
    html = models.TextField(blank=True, null=True)
    update_date = models.DateTimeField(default=timezone.now, verbose_name="Updated")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Parent page",
    )
    full_path = models.CharField(
        max_length=525, editable=False, verbose_name="Full path"
    )
    show_in_nav = models.BooleanField(default=False, verbose_name="Show in nav")
    ranking = models.FloatField(default=0.0, editable=False)

    def update_full_path(self):
        if self.parent:
            self.full_path = f"{self.parent.full_path}/{slugify(self.title)}"
        else:
            self.full_path = slugify(self.title)

    def save(self, *args, **kwargs):
        self.html = self.html if self.html else utilities.render_html(self.text)
        self.update_date = timezone.now().replace(microsecond=0)
        self.update_full_path()
        super(Page, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # update child pages' full_path before deleting the parent
        children = Page.objects.filter(parent=self)
        for child in children:
            child.parent = None
            child.save()
        super(Page, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"path": self.full_path})

    def __str__(self):
        return self.title

    class Meta:
        db_table = "cp_pages"
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ["title"]
