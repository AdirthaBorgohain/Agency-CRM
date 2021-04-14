# Generated by Django 3.1.5 on 2021-04-13 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('agent_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=12, unique=True)),
                ('commission', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('deductions', models.FloatField(default=0)),
                ('prev_balance', models.FloatField()),
                ('grand_total', models.FloatField()),
                ('is_paid', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.agent')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('additional_charges', models.FloatField(default=0)),
                ('grand_total', models.FloatField()),
                ('is_paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('language', models.CharField(choices=[('Assamese', 'Assamese'), ('English', 'English'), ('Hindi', 'Hindi'), ('Bengali', 'Bengali'), ('Others', 'Others')], default='Assamese', max_length=10)),
                ('category', models.CharField(choices=[('Newspaper', 'Newspaper'), ('Magazine', 'Magazine')], default='Newspaper', max_length=10)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('net_price', models.FloatField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='entities.product')),
            ],
        ),
        migrations.CreateModel(
            name='BillDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('net_price', models.FloatField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.bill')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='entities.product')),
            ],
        ),
    ]