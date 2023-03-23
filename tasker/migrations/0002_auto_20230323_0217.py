from django.db import migrations


def load_initial_data(apps, schema_editor):
    tag_model = apps.get_model('tasker', 'Tag')
    tag_model.objects.create(name="home")
    tag_model.objects.create(name="work")
    tag_model.objects.create(name="shop")

    home = tag_model.objects.get(id=1)
    work = tag_model.objects.get(id=2)
    shop = tag_model.objects.get(id=3)

    task_model = apps.get_model('tasker', 'Task')
    task1 = task_model.objects.create(
        content="Buy 3 carrots and 1 pineapple",
    )
    task1.task_tag.add(shop)

    task2 = task_model.objects.create(
        content="Clean windows",
    )
    task2.task_tag.add(shop, home)

    task3 = task_model.objects.create(
        content="Complete project",
    )
    task3.task_tag.add(work)


class Migration(migrations.Migration):
    dependencies = [
        ("tasker", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_initial_data)]
