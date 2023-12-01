# Generated by Django 4.2.4 on 2023-09-01 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0003_alter_page_options_alter_page_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="send_to_archive",
            field=models.BooleanField(default=True, verbose_name="Archive post"),
        ),
        migrations.AddField(
            model_name="post",
            name="send_to_fediverse",
            field=models.BooleanField(default=True, verbose_name="Federate post"),
        ),
        migrations.AlterField(
            model_name="post",
            name="create_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Created"),
        ),
    ]
