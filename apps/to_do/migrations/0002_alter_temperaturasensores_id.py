# Generated by Django 5.0.6 on 2024-06-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperaturasensores',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]