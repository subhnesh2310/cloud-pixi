# Generated by Django 3.2.25 on 2024-05-16 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectNE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(default=None, max_length=100)),
                ('username', models.CharField(default='temp', max_length=100)),
                ('password', models.CharField(default='root', max_length=100)),
                ('hostname', models.CharField(default=None, max_length=100)),
                ('port_number', models.IntegerField(default=22)),
                ('interface', models.CharField(default='CLI', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DiconnectNE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(blank=True, default='', max_length=100)),
                ('username', models.CharField(default='temp', max_length=100)),
                ('password', models.CharField(default='root', max_length=100)),
                ('hostname', models.CharField(default=None, max_length=100)),
                ('port_number', models.IntegerField(default=22)),
                ('interface', models.CharField(default='CLI', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SendRCV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(default='CLI', max_length=100)),
                ('command', models.CharField(blank=True, max_length=100, null=True)),
                ('timeout', models.IntegerField(default=20)),
                ('confirmI', models.BooleanField(default=False)),
                ('step', models.BooleanField(default=False)),
                ('match', models.CharField(blank=True, max_length=100, null=True)),
                ('poll', models.BooleanField(default=False)),
                ('stash', models.CharField(blank=True, max_length=100, null=True)),
                ('mode', models.CharField(default='ssh', max_length=10)),
                ('sendOnly', models.BooleanField(default=False)),
                ('rcvOnly', models.BooleanField(default=False)),
            ],
        ),
    ]