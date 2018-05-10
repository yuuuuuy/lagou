"""Peewee migrations -- 001_migration_name.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class Position(pw.Model):
        position_name = pw_pext.CharField(null=False)
        city = pw_pext.CharField(null=True)
        business_zones = pw_pext.ArrayField(
            pw_pext.CharField,
            default=[],
            null=True)
        company_full_name = pw_pext.CharField(null=True)
        company_short_name = pw_pext.CharField(null=True)
        company_lable_list = pw_pext.ArrayField(
            pw_pext.CharField,
            default=[],
            null=True)
        company_size = pw_pext.CharField(null=True)
        education = pw_pext.CharField(null=True)
        finance_stage = pw_pext.CharField(null=True)
        first_type = pw_pext.CharField(null=True)
        industry_field = pw_pext.CharField(null=True)
        job_nature = pw_pext.CharField(null=True)
        position_lables = pw_pext.ArrayField(
            pw_pext.CharField,
            default=[],
            null=True)
        salary = pw_pext.CharField(null=True)
        salary_max = pw_pext.IntegerField(null=True)
        salary_min = pw_pext.IntegerField(null=True)
        salary_avg = pw_pext.IntegerField(null=True)
        second_type = pw_pext.CharField(null=True)
        work_year = pw_pext.CharField(null=True)

        class Meta:
            db_table = "position"


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

