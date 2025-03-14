# Generated by Django 5.0.4 on 2025-01-25 05:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_friendship_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userthread',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='userthread',
            name='thread',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='body',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='message',
            name='coords',
        ),
        migrations.RemoveField(
            model_name='message',
            name='datetime',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='title',
        ),
        migrations.AddField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tagged_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('UNREAD', 'Unread'), ('READ', 'Read')], default='UNREAD', max_length=50),
        ),
        migrations.AddField(
            model_name='notification',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='threads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='thread',
            name='thread_type',
            field=models.CharField(choices=[('PRIVATE', 'Private'), ('HOOD', 'Hood')], default='HOOD', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friendship',
            name='status',
            field=models.CharField(choices=[('REQUESTED', 'Requested'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='REQUESTED', max_length=10),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='main.thread'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='hood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='main.hood'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user'], name='main_notifi_user_id_bf2afc_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['status'], name='main_notifi_status_edd725_idx'),
        ),
        migrations.AlterModelTable(
            name='thread',
            table=None,
        ),
        migrations.DeleteModel(
            name='UserThread',
        ),
    ]
