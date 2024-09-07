from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_auto_20240902_2113"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "default_related_name": "posts",
                "ordering": ("-pub_date",),
                "verbose_name": "публикация",
                "verbose_name_plural": "Публикации",
            },
        ),
    ]
