# Generated by Django 4.2.4 on 2023-09-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0004_post_send_to_archive_post_send_to_fediverse_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="ranking",
            field=models.FloatField(default=0.0, editable=False),
        ),
        migrations.AddField(
            model_name="post",
            name="ranking",
            field=models.FloatField(default=0.0, editable=False),
        ),
    ]
