from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(blank=True, null=True, auto_now=True)),
                ('created_id', models.IntegerField()),
                ('modified_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'customers',
            },
        ),
    ]