# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class MySQLPipeline:
    def __init__(self, mysql_host, mysql_port, mysql_user, mysql_password, mysql_database):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_database=crawler.settings.get('MYSQL_DATABASE')
        )

    def open_spider(self, spider):
        # 连接到MySQL数据库
        self.conn = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            database=self.mysql_database,
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()
        # 创建表（如果不存在）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                star VARCHAR(255),
                critical VARCHAR(255)
            )
        ''')

    def process_item(self, item, spider):
        # 将数据插入到MySQL数据库中
        sql = "INSERT INTO movies (title, star, critical) VALUES (%s, %s, %s)"
        values = (item['title'], item['star'], item['critical'])
        self.cursor.execute(sql, values)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # 关闭数据库连接
        self.cursor.close()
        self.conn.close()

