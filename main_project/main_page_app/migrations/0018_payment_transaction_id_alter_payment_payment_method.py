# Generated by Django 5.1.5 on 2025-03-31 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page_app', '0017_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('esewa', 'eSewa'), ('khalti', 'Khalti')], max_length=20),
        ),
    ]
