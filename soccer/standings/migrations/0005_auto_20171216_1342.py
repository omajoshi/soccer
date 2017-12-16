# Generated by Django 2.0 on 2017-12-16 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standings', '0004_auto_20171216_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='league',
            field=models.CharField(blank=True, choices=[('fra', 'France'), ('ger', 'Germany'), ('ita', 'Italy'), ('esp', 'Spain'), ('eng', 'England')], max_length=3),
        ),
        migrations.AlterField(
            model_name='team',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='standings.Owner'),
        ),
    ]
