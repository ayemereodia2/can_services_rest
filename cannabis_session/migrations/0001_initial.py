# Generated by Django 5.0.1 on 2024-02-17 03:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("activity_name", models.CharField(max_length=50)),
                ("activity_icon_id", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Emotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("emotion_name", models.CharField(max_length=50)),
                ("emotion_icon_id", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="SessionFeedBack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.CharField(max_length=10)),
                ("feeling", models.CharField(max_length=20)),
                ("optional_notes", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="SubEmotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sub_emotion_name", models.CharField(max_length=50)),
                ("emotion_icon_id", models.CharField(max_length=100)),
                (
                    "main_emotions",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cannabis_session.emotion",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserActivitySession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("activity_duration", models.CharField(max_length=50)),
                ("activity_state", models.CharField(max_length=50)),
                ("pub_date", models.DateTimeField(auto_now=True)),
                (
                    "activity_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cannabis_session.activity",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserConsumptionSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_duration", models.CharField(max_length=50)),
                ("session_quantity", models.CharField(max_length=50)),
                ("session_state", models.CharField(max_length=50)),
                ("added_item_to_stash", models.BooleanField()),
                ("stash_id", models.CharField(max_length=50)),
                ("pub_date", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserCompleteSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pub_date", models.DateTimeField(auto_now=True)),
                (
                    "activity_by",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cannabis_session.useractivitysession",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "feedback",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cannabis_session.sessionfeedback",
                    ),
                ),
                (
                    "consumption_by",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cannabis_session.userconsumptionsession",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="emotion",
            name="user_consumption_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="cannabis_session.userconsumptionsession",
            ),
        ),
    ]
