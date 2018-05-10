from playhouse import postgres_ext
from playhouse.postgres_ext import PostgresqlExtDatabase, Model
from peewee_migrate import Router

from lagou.settings import DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD


database = PostgresqlExtDatabase(database=DB_DATABASE,
                                 host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 autocommit=True,
                                 autorollback=True)


router = Router(database)


class BaseModel(Model):
    class Meta:
        database = database


class Position(BaseModel):
    position_name = postgres_ext.CharField(
        verbose_name='职位名称',
        max_length=255,
        null=False)
    city = postgres_ext.CharField(
        verbose_name='城市',
        max_length=255,
        null=True)
    # 工作地点
    business_zones = postgres_ext.ArrayField(
        postgres_ext.CharField,
        default=[],
        null=True)
    company_full_name = postgres_ext.CharField(
        verbose_name='公司全称',
        max_length=255,
        null=True)
    company_short_name = postgres_ext.CharField(
        verbose_name='公司简称',
        max_length=255,
        null=True)
    company_lable_list = postgres_ext.ArrayField(
        postgres_ext.CharField,
        default=[],
        null=True)
    company_size = postgres_ext.CharField(
        verbose_name='公司规模(人)',
        max_length=255,
        null=True)
    education = postgres_ext.CharField(
        verbose_name='学历',
        max_length=255,
        null=True)
    finance_stage = postgres_ext.CharField(
        verbose_name='公司财务情况(A轮)',
        max_length=255,
        null=True)
    first_type = postgres_ext.CharField(
        verbose_name='一级分类(如后端、前端)',
        max_length=255,
        null=True)
    industry_field = postgres_ext.CharField(
        verbose_name='公司领域',
        max_length=255,
        null=True)
    job_nature = postgres_ext.CharField(
        verbose_name='工作性质(全职or实习)',
        max_length=255,
        null=True)
    position_lables = postgres_ext.CharField(
        postgres_ext.CharField,
        default=[],
        null=True)
    salary = postgres_ext.CharField(
        verbose_name='薪资范围',
        max_length=255,
        null=True)
    salary_max = postgres_ext.IntegerField(
        verbose_name='最高薪资',
        null=True)
    salary_min = postgres_ext.IntegerField(
        verbose_name='最低薪资',
        null=True)
    salary_avg = postgres_ext.IntegerField(
        verbose_name='平均薪资',
        null=True)
    second_type = postgres_ext.CharField(
        verbose_name='二级分类(如 java、python)',
        max_length=255,
        null=True)
    work_year = postgres_ext.CharField(
        verbose_name='工作年限',
        max_length=255,
        null=True)


if __name__ == '__main__':
    # Create migration
    # router.create('migration_name')

    # Run migration/migrations
    # router.run('migration_name')

    # Run all unapplied migrations
    # router.run()
    pass
