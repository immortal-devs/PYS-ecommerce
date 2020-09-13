# Generated by Django 3.1.1 on 2020-09-13 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='firstname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='lastname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='mobile_no',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.address'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
