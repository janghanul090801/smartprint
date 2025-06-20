# Generated by Django 5.1.1 on 2024-10-20 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_businessnumber_customuser_exponent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(default='somewhere', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='detailAddress',
            field=models.CharField(default='4층', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='firstNumber',
            field=models.CharField(choices=[('010', '010'), ('011', '011'), ('016', '016'), ('017', '017'), ('019', '019')], default='010', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='lastNumber',
            field=models.IntegerField(default=2222),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='middleNumber',
            field=models.IntegerField(default=2222),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='postcode',
            field=models.CharField(default='06134', max_length=10),
            preserve_default=False,
        ),
    ]
