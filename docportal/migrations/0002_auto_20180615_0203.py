# Generated by Django 2.0.6 on 2018-06-15 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docportal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ManufacturedUnitModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='doc_type',
            field=models.CharField(choices=[('00', 'UserManual'), ('01', 'ProgressPhotos'), ('02', 'TestingResults')], default='00', max_length=10),
        ),
        migrations.AddField(
            model_name='documentpermission',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docportal.DocumentModel'),
        ),
        migrations.AddField(
            model_name='documentpermission',
            name='viewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docportal.ManufacturedUnitModel'),
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='viewers',
            field=models.ManyToManyField(through='docportal.DocumentPermission', to=settings.AUTH_USER_MODEL),
        ),
    ]
