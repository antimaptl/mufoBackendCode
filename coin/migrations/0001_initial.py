# Generated by Django 4.2.20 on 2025-07-26 07:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        ('Jockey_club_owner', '0001_initial'),
        ('master', '0004_alter_common_phone'),
        ('Audio_Jockey', '0001_initial'),
        ('Coins_club_owner', '0001_initial'),
        ('Coins_trader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift_image', models.ImageField(upload_to='gifts/')),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User_to_Audio_Jockey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.user')),
                ('to_Audio_Jockey', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Audio_Jockey.audio_jockey')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_coins', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.common')),
            ],
        ),
        migrations.CreateModel(
            name='Coins_trader_to_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_trader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coins_trader.coins_trader')),
                ('to_User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.user')),
            ],
        ),
        migrations.CreateModel(
            name='Coins_trader_to_Jockey_club_owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_trader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coins_trader.coins_trader')),
                ('to_Jockey_club_owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jockey_club_owner.jockey_club_owner')),
            ],
        ),
        migrations.CreateModel(
            name='Coins_club_owner_to_Coins_trader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coins_club_owner.coins_club_owner')),
                ('to_trader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Coins_trader.coins_trader')),
            ],
        ),
        migrations.CreateModel(
            name='Admin_to_Coins_club_owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numcoin', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('Coins_Club_Owner_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coins_club_owner.coins_club_owner')),
            ],
        ),
    ]
