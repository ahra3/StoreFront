# Generated by Django 5.1.5 on 2025-02-24 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_zip_address_zipi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='desc',
            new_name='description',
        ),
    ]
