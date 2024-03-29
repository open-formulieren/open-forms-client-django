# Generated by Django 4.1.1 on 2022-09-24 09:58

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Configuration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "api_root",
                    models.URLField(
                        help_text="The root URL of the Open Forms API. Example: https://forms.example.com/api/v1/",
                        verbose_name="API root URL",
                    ),
                ),
                (
                    "api_token",
                    models.CharField(
                        blank=True,
                        help_text="The Open Forms API token value. Example: 7ab84e80b3d68d52a5f9e1712e3d0eda27d21e58",
                        max_length=128,
                        verbose_name="API Token",
                    ),
                ),
                (
                    "sdk_css_url",
                    models.URLField(
                        blank=True,
                        help_text="The Open Forms SDK stylesheet URL. Example: https://forms.example.com/static/sdk/open-forms-sdk.css",
                        verbose_name="SDK CSS URL",
                    ),
                ),
                (
                    "sdk_js_url",
                    models.URLField(
                        blank=True,
                        help_text="The Open Forms SDK JavaScript URL. Example: https://forms.example.com/static/sdk/open-forms-sdk.js",
                        verbose_name="SDK JS URL",
                    ),
                ),
                (
                    "use_sentry",
                    models.BooleanField(
                        default=False,
                        help_text="When enabled and Sentry is installed, Open Forms SDK errors will be sent to the configured Sentry instance.",
                        verbose_name="Use Sentry",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
