# Generated by Django 2.2 on 2019-05-14 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190507_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/None/default.png', upload_to=''),
        ),
    ]