# Generated by Django 5.1.7 on 2025-03-25 03:50

import django.db.models.deletion
import report.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenSpace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('easting', models.FloatField(blank=True, null=True)),
                ('northing', models.FloatField(blank=True, null=True)),
                ('utm_zone', models.CharField(blank=True, max_length=10, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('area_size', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('region', models.CharField(default='Dar es Salaam', max_length=100)),
                ('district', models.CharField(default='Kinondoni', max_length=100)),
                ('ward', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('managed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_info', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference_id', models.CharField(default=report.models.generate_reference_id, editable=False, max_length=8, unique=True)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('vandalism', 'Vandalism'), ('littering', 'Littering'), ('unauthorized_activity', 'Unauthorized Activity'), ('illegal_dumping', 'Illegal Dumping'), ('other', 'Other')], max_length=50)),
                ('date_reported', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('under_investigation', 'Under Investigation'), ('resolved', 'Resolved')], default='pending', max_length=20)),
                ('assigned_to', models.CharField(blank=True, max_length=100, null=True)),
                ('resolution_date', models.DateField(blank=True, null=True)),
                ('open_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_space', to='report.openspace')),
                ('reported_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
