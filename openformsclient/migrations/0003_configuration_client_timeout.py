# Generated by Django 3.2.23 on 2024-02-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("openformsclient", "0002_alter_configuration_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="configuration",
            name="client_timeout",
            field=models.PositiveIntegerField(
                default=5,
                help_text="The timeout that is used for requests (in seconds)",
                verbose_name="Client request timeout",
            ),
        ),
    ]
