# Generated by Django 5.0.6 on 2024-06-28 09:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_rename_salary_post_balance_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="address",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
