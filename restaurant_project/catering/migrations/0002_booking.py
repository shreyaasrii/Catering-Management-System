# Generated by Django 5.0.6 on 2024-07-30 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('details', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
