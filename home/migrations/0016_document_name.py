# Generated by Django 2.0.2 on 2018-02-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_document_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]