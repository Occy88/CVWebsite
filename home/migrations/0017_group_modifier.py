# Generated by Django 2.0.2 on 2018-02-14 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_document_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='modifier',
            field=models.IntegerField(default=1),
        ),
    ]
