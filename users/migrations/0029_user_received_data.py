# Generated by Django 3.2 on 2021-06-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_remove_user_received_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='received_data',
            field=models.BooleanField(default=False, verbose_name='We have received data from this subject'),
        ),
    ]
