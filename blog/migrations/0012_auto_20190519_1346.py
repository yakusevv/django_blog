# Generated by Django 2.2 on 2019-05-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='/profiles/None/default.png', upload_to='profiles/'),
        ),
    ]
