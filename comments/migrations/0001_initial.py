# Generated by Django 2.0 on 2020-03-12 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_body', models.CharField(max_length=60)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
        ),
    ]
