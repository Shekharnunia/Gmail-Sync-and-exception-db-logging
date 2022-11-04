# Generated by Django 3.2.16 on 2022-11-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail_messages', '0002_mail_snippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.PositiveIntegerField()),
                ('error_stack', models.TextField(null=True)),
            ],
        ),
    ]
