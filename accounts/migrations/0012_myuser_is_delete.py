# Generated by Django 4.2.2 on 2023-07-06 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_relationship_follower_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
    ]
