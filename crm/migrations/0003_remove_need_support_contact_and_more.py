# Generated by Django 4.0.3 on 2022-03-29 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0002_contract_event_alter_customer_sales_contact_need_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='support_contact',
        ),
        migrations.AlterField(
            model_name='customer',
            name='sales_contact',
            field=models.ForeignKey(limit_choices_to={'profile_staff': 2}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='support_contact',
            field=models.ForeignKey(limit_choices_to={'profile_staff': 3}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
