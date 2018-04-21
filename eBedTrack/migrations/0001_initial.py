# Generated by Django 2.0.4 on 2018-04-21 21:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('bed_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('bed_type', models.CharField(choices=[('ICU/CC', 'ICU/CC'), ('Emergency Unit', 'EU'), ('MED/SURG', 'MED/SURG'), ('OB', 'OB'), ('SICU', 'SICU'), ('Neg-Pres/Iso', 'Neg-Pres/Iso'), ('OR', 'OR'), ('Peds', 'Peds'), ('PICU', 'PICU'), ('NICU', 'NICU'), ('Burn', 'Burn'), ('Mental-Health', 'Mental-Health'), ('Other', 'Other')], default='ICU', max_length=50)),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='VACANT', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BlockBed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Reserved', max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('phone_no', models.CharField(max_length=50)),
                ('bed_type', models.CharField(blank=True, choices=[('ICU/CC', 'ICU/CC'), ('EU', 'EU'), ('MED/SURG', 'MED/SURG'), ('OB', 'OB'), ('SICU', 'SICU'), ('Neg-Pres/Iso', 'Neg-Pres/Iso'), ('OR', 'OR'), ('Peds', 'Peds'), ('PICU', 'PICU'), ('NICU', 'NICU'), ('Burn', 'Burn'), ('Mental-Health', 'Mental-Health'), ('Other', 'Other')], default='ICU', max_length=50)),
                ('message', models.TextField()),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('contactId', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('emailId', models.CharField(max_length=50)),
                ('question', models.TextField()),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('hospital_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('hospital_name', models.CharField(max_length=100)),
                ('city', models.CharField(default='UNKNOWN', max_length=100)),
                ('county', models.CharField(default='UNKNOWN', max_length=100)),
                ('state', models.CharField(default='UNKNOWN', max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('phone_no', models.CharField(max_length=12)),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=300)),
                ('county', models.CharField(max_length=300)),
                ('state', models.CharField(max_length=300)),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('nurse_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('phone_no', models.CharField(max_length=20)),
                ('created_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=32)),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosnurses', to='eBedTrack.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_tag', models.CharField(default=0, max_length=20, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sex', models.CharField(blank=True, choices=[('M', 'MALE'), ('F', 'FEMALE')], default='M', max_length=10)),
                ('time_of_admission', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('condition', models.CharField(choices=[('Undetermined', 'Undetermined'), ('Good', 'Good'), ('Fair', 'Fair'), ('Serious', 'Serious'), ('Critical', 'Critical'), ('Dead', 'Dead')], default='Undetermined', max_length=50)),
                ('bed_type', models.CharField(blank=True, choices=[('ICU/CC', 'ICU/CC'), ('Emergency Unit', 'EU'), ('MED/SURG', 'MED/SURG'), ('OB', 'OB'), ('SICU', 'SICU'), ('Neg-Pres/Iso', 'Neg-Pres/Iso'), ('OR', 'OR'), ('Peds', 'Peds'), ('PICU', 'PICU'), ('NICU', 'NICU'), ('Burn', 'Burn'), ('Mental-Health', 'Mental-Health'), ('Other', 'Other')], default='Emergency Unit', max_length=50)),
                ('bed_id', models.CharField(max_length=50, unique=True)),
                ('mode_of_arrival', models.CharField(blank=True, max_length=50)),
                ('age', models.CharField(blank=True, max_length=10, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('injuries', models.CharField(blank=True, max_length=50)),
                ('deposition', models.CharField(blank=True, max_length=50)),
                ('time_of_surgery', models.CharField(blank=True, max_length=20)),
                ('kin_name', models.CharField(blank=True, max_length=50)),
                ('relation', models.CharField(blank=True, max_length=50)),
                ('time_of_death', models.CharField(blank=True, max_length=20)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('patient_status', models.CharField(blank=True, choices=[('Admitted', 'Admitted'), ('Discharged', 'Discharged')], default='Admitted', max_length=40)),
                ('hospital_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosppatients', to='eBedTrack.Hospital')),
            ],
        ),
        migrations.AddField(
            model_name='blockbed',
            name='hospital_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eBedTrack.Hospital'),
        ),
        migrations.AddField(
            model_name='bed',
            name='bh',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosbeds', to='eBedTrack.Hospital'),
        ),
    ]
