# Generated by Django 3.1.5 on 2021-01-26 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comentarios_ofertas'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comentarios',
            new_name='Comentario',
        ),
        migrations.RenameModel(
            old_name='Ofertas',
            new_name='Oferta',
        ),
    ]
