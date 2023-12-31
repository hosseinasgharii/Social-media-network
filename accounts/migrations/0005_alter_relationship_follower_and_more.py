# Generated by Django 4.2.2 on 2023-06-20 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_relations', related_query_name='following_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_relations', related_query_name='follower_relation', to=settings.AUTH_USER_MODEL),
        ),
    ]
