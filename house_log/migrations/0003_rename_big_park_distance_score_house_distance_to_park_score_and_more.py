# Generated by Django 4.1.5 on 2023-02-22 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house_log', '0002_house_archive_alter_profile_friend_addresses_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='big_park_distance_score',
            new_name='distance_to_park_score',
        ),
        migrations.RemoveField(
            model_name='house',
            name='distance_to_friends_score',
        ),
        migrations.RemoveField(
            model_name='house',
            name='park_bool',
        ),
        migrations.RemoveField(
            model_name='house',
            name='park_name',
        ),
        migrations.RemoveField(
            model_name='house',
            name='park_walk_dist',
        ),
        migrations.RemoveField(
            model_name='house',
            name='small_park_distance_score',
        ),
        migrations.RemoveField(
            model_name='house',
            name='sports_complex_score',
        ),
        migrations.RemoveField(
            model_name='house',
            name='storage_space_notes',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='friend_addresses',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='houses',
        ),
        migrations.AlterField(
            model_name='house',
            name='type_of_home',
            field=models.IntegerField(blank=True, choices=[(1, 'House'), (2, 'Split House'), (3, 'Apartment')], null=True),
        ),
        migrations.DeleteModel(
            name='Friend_Address',
        ),
    ]