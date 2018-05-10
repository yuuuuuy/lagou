# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from lagou.models import database as db
import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase
from lagou.settings import DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD


class LagouPipeline(object):
    def __init__(self):
        self.db = db

    def process_item(self, item, spider):
        print(item)
        sql = "INSERT INTO position(position_name,city,business_zones," \
              "company_full_name,company_short_name,company_lable_list," \
              "company_size,education,finance_stage,first_type,industry_field," \
              "job_nature,position_lables,salary,salary_max,salary_min," \
              "salary_avg,second_type,work_year) VALUES (" \
              "'{item[position_name]}'," \
              "'{item[city]}'," \
              "ARRAY{item[business_zones]}," \
              "'{item[company_full_name]}'," \
              "'{item[company_short_name]}'," \
              "ARRAY{item[company_lable_list]}," \
              "'{item[company_size]}','{item[education]}'," \
              "'{item[finance_stage]}'," \
              "'{item[first_type]}'," \
              "'{item[industry_field]}'," \
              "'{item[job_nature]}'," \
              "ARRAY{item[position_lables]}," \
              "'{item[salary]}'," \
              "{item[salary_max]}," \
              "{item[salary_min]}," \
              "{item[salary_avg]}," \
              "'{item[second_type]}','{item[work_year]}')".format(item=item)
        print(sql)
        try:
            self.db.execute_sql(sql)
            self.db.commit()
        except peewee.IntegrityError:
            self.db.rollback()
        except (peewee.OperationalError, peewee.InterfaceError):
            self.db.close()
            self.db = PostgresqlExtDatabase(database=DB_DATABASE,
                                            host=DB_HOST,
                                            user=DB_USER,
                                            password=DB_PASSWORD,
                                            autocommit=True,
                                            autorollback=True)
            self.db.execute_sql(sql)
            self.db.commit()

        return item
