# Generated by Django 5.0.7 on 2024-08-06 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_project_comment_taskassignment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='taskassignment',
            unique_together=set(),
        ),
    ]
