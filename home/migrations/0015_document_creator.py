# Generated by Django 2.0.2 on 2018-02-14 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_log_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='creator',
            field=models.IntegerField(default=1),
        ),
    ]