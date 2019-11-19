# Generated by Django 2.2.7 on 2019-11-15 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_auto_20191115_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='The bucket name for the to-do', max_length=200)),
                ('user', models.ForeignKey(help_text='The user id who created this bucket', on_delete=django.db.models.deletion.CASCADE, to='account.User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
