from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_auto_20240902_1547"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Изображение"
            ),
        ),
    ]
