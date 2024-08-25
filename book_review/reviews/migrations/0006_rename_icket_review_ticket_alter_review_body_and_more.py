# Generated by Django 5.1 on 2024-08-25 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_remove_review_ticket_review_icket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='icket',
            new_name='ticket',
        ),
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
    ]