# Generated by Django 2.2.16 on 2021-03-06 00:11

from django.db import migrations, models
import django.db.models.deletion
from datetime import datetime


def convert_tags_and_attributes(apps, schema_editor):
    Attribute = apps.get_model("typeclasses", "Attribute")
    Tag = apps.get_model("typeclasses", "Tag")
    Permanence = apps.get_model("object_extensions", "Permanence")
    Dimensions = apps.get_model("object_extensions", "Dimensions")

    # set deleted objects
    qs = Attribute.objects.filter(db_key="deleted_time").prefetch_related(
        "objectdb_set"
    )
    permanence_objects = {}
    for attr in qs:
        try:
            objdb = attr.objectdb_set.all()[0]
            # using a dict with pks as keys to prevent duplicates
            permanence_objects[objdb.pk] = Permanence(
                objectdb=objdb, deleted_time=datetime.now()
            )
        except IndexError:
            pass
    qs.delete()
    Permanence.objects.bulk_create(permanence_objects.values())

    # set capacity for containers
    qs = Attribute.objects.filter(
        db_key__in=["max_volume", "num_living"],
        objectdb__db_typeclass_path__in=[
            "typeclasses.containers.container.Container",
            "typeclasses.wearable.wearable.WearableContainer",
            "typeclasses.npcs.npc.MultiNpc",
            "typeclasses.npcs.npc.Agent",
        ],
    ).prefetch_related("objectdb_set")
    dimensions_objects = {}
    for attr in qs:
        try:
            objdb = attr.objectdb_set.all()[0]
            value = attr.db_value
            dimensions = dimensions_objects.get(objdb.pk, Dimensions(objectdb=objdb))
            if attr.db_key == "max_volume":
                dimensions.capacity = value
            else:
                dimensions.quantity = value
            dimensions_objects[objdb.pk] = dimensions
        except IndexError:
            pass
    Dimensions.objects.bulk_create(dimensions_objects.values())
    Tag.objects.filter(db_key="deleted").delete()
    Attribute.objects.filter(
        db_key__in=["put_time", "volume", "max_volume", "num_instances", "num_living"]
    ).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("objects", "0011_auto_20191025_0831"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dimensions",
            fields=[
                (
                    "objectdb",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="objects.ObjectDB",
                    ),
                ),
                (
                    "size",
                    models.PositiveIntegerField(
                        null=True,
                        help_text="The amount of space this object takes up inside a container.",
                    ),
                ),
                (
                    "weight",
                    models.PositiveIntegerField(
                        null=True, help_text="How heavy this object is."
                    ),
                ),
                ("capacity", models.PositiveIntegerField(null=True)),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        default=1,
                        help_text="How many copies of this item there are, for stackable objects.",
                    ),
                ),
            ],
            options={"abstract": False, "verbose_name_plural": "Dimensions"},
        ),
        migrations.CreateModel(
            name="Permanence",
            fields=[
                (
                    "objectdb",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="objects.ObjectDB",
                    ),
                ),
                (
                    "put_time",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="time.time() value of when an object was moved, used for sorting. We use integer time value here rather than datetime to prevent errors from null.",
                    ),
                ),
                (
                    "deleted_time",
                    models.DateTimeField(
                        help_text="If set, this timestamp means an object is marked for deletion.",
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False, "verbose_name_plural": "Permanence"},
        ),
        migrations.RunPython(
            convert_tags_and_attributes, migrations.RunPython.noop, elidable=False
        ),
    ]
