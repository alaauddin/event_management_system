# Generated by Django 4.2 on 2023-11-23 12:52

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
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to='images/events/')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('canceled', 'Canceled')], default='draft', max_length=20)),
                ('discout', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Event.participant')),
                ('registration_type', models.CharField(max_length=50)),
            ],
            bases=('Event.participant',),
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Event.event')),
                ('theme', models.CharField(max_length=100)),
            ],
            bases=('Event.event',),
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Event.participant')),
                ('position', models.CharField(max_length=50)),
            ],
            bases=('Event.participant',),
        ),
        migrations.CreateModel(
            name='SocialEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Event.event')),
                ('activities', models.TextField()),
            ],
            bases=('Event.event',),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Event.participant')),
                ('expertise', models.CharField(max_length=255)),
            ],
            bases=('Event.participant',),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Event.participant')),
                ('tasks', models.TextField()),
            ],
            bases=('Event.participant',),
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Event.event')),
                ('topic', models.CharField(max_length=100)),
            ],
            bases=('Event.event',),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='Event.event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='Event.participant')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='Event.location'),
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendas', to='Event.event')),
            ],
        ),
    ]
