# Generated by Django 4.2.5 on 2023-11-01 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aintdoinit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField()),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aintdoinit.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aintdoinit.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aintdoinit.size')),
            ],
        ),
        migrations.DeleteModel(
            name='Mod',
        ),
    ]