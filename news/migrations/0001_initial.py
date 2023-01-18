# Generated by Django 4.1.5 on 2023-01-12 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rating', models.IntegerField(default=0)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], default='NW', max_length=2)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('post_header', models.CharField(max_length=90)),
                ('post_text', models.TextField()),
                ('post_rating', models.IntegerField(default=0)),
                ('author_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bumaga.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bumaga.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bumaga.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_category',
            field=models.ManyToManyField(through='bumaga.PostCategory', to='bumaga.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=255)),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
                ('comment_rating', models.IntegerField(default=0)),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bumaga.post')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]