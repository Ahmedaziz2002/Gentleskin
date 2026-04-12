from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_affiliateclick_session_key"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["name"], "verbose_name_plural": "Categories"},
        ),
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[("draft", "Draft"), ("published", "Published")],
                db_index=True,
                default="draft",
                max_length=10,
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["status", "created_at"], name="blog_post_status_701356_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["category", "status"], name="blog_post_categor_7f0b6a_idx"),
        ),
        migrations.AddIndex(
            model_name="affiliateclick",
            index=models.Index(fields=["post", "clicked_at"], name="blog_affili_post_id_d17dc4_idx"),
        ),
        migrations.AddIndex(
            model_name="affiliateclick",
            index=models.Index(fields=["session_key", "clicked_at"], name="blog_affili_session_4ae124_idx"),
        ),
    ]
