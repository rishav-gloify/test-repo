# Generated for adding searchable authors while preserving existing book data.
import django.db.models.deletion
from django.db import migrations, models


def move_author_names_to_author_model(apps, schema_editor):
    Author = apps.get_model("books", "Author")
    Book = apps.get_model("books", "Book")

    for book in Book.objects.all().iterator():
        author_name = (book.author or "Unknown Author").strip() or "Unknown Author"
        author, _ = Author.objects.get_or_create(name=author_name)
        book.author_ref_id = author.pk
        book.save(update_fields=["author_ref"])


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="book",
            name="author_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="books",
                to="books.author",
            ),
        ),
        migrations.RunPython(
            move_author_names_to_author_model,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="book",
            name="author",
        ),
        migrations.RenameField(
            model_name="book",
            old_name="author_ref",
            new_name="author",
        ),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="books",
                to="books.author",
            ),
        ),
        migrations.AlterModelOptions(
            name="book",
            options={"ordering": ["title", "author__name"]},
        ),
    ]
