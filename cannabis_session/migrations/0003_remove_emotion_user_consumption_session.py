# Generated by Django 5.0.1 on 2024-02-17 04:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cannabis_session", "0002_userconsumptionsession_emotion_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="emotion",
            name="user_consumption_session",
        ),
    ]
