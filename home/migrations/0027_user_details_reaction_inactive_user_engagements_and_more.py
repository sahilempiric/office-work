# Generated by Django 4.0.4 on 2022-06-14 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_remove_engagements_user_remove_inactive_user_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='reaction',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='inactive_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
        migrations.CreateModel(
            name='Engagements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=0)),
                ('reaction', models.CharField(default='-', max_length=255)),
                ('engagement_on', models.CharField(default='-', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
        migrations.CreateModel(
            name='comment_view',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('comment_on', models.CharField(default='-', max_length=255)),
                ('view_on', models.CharField(default='-', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
    ]
