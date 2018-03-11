# Generated by Django 2.0.3 on 2018-03-11 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
        ('filterers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filterertopolitician',
            old_name='accepted',
            new_name='accepted_by_filterer',
        ),
        migrations.AddField(
            model_name='filterertopolitician',
            name='accepted_by_politician',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='messagetag',
            name='issue',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='issues.Issue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messagetag',
            name='stance',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='issues.Stance'),
            preserve_default=False,
        ),
    ]