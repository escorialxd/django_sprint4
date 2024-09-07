from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0009_alter_comment_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "default_related_name": "comments",
                "ordering": ("created_at",),
                "verbose_name": "комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="pub_date",
            new_name="created_at",
        ),
    ]
