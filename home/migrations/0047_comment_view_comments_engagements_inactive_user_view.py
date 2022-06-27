# Generated by Django 3.2.3 on 2022-06-21 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_auto_20220621_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='view',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views_on', models.CharField(default='-', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
        migrations.CreateModel(
            name='inactive_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NOT AUTHORIZED', 'NOT AUTHORIZED'), ('FLOOD WAIT', 'FLOOD WAIT'), ('BANNED', 'BANNED'), ('DELETED', 'DELETED'), ('NEED PASSWORD', 'NEED PASSWORD')], default='ACTIVE', max_length=255)),
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
                ('message_on', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='-')),
                ('comment_on', models.CharField(default='-', max_length=255)),
                ('message_on', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
        migrations.CreateModel(
            name='comment_view',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='-')),
                ('views', models.IntegerField(default=0)),
                ('comment_on', models.CharField(default='-', max_length=255)),
                ('view_on', models.CharField(default='-', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
    ]
