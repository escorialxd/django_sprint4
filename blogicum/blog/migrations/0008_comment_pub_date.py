import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0007_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата",
            ),
            preserve_default=False,
        ),
    ]
