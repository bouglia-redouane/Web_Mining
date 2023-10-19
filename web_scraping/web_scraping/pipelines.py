# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class WebScrapingPipeline:
    def process_item(self, item, spider):
        return item

class SaveToMySQLPipeline:
    db_config = {
        'host': 'localhost',
        'user': 'redouane',
        'password': 'Azertyuiop@123',
        'database': 'web_scraping',

    }
    conn = None
    cur = None
    def __init__(self):

        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cur = self.conn.cursor()
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS linkedin_posts(
                            id bigint primary key,
                            job_url TEXT ,
                            job_title TEXT ,
                            company TEXT,
                            location TEXT,
                            company_url TEXT,
                            job_description TEXT,
                            date varchar(20)
                            )
                        """)
        except mysql.connector.Error as error:
            print('*************************************************************')
            print(f"Error: {error}")
            print('*************************************************************')


    def process_item(self, item, spider):
        id = self.string_to_id(item['job_url'])
        if self.check_if_exist(id) == False:
            tmp = self.clean_item(item)
            self.cur.execute("""
                insert into linkedin_posts(id,job_url, job_title, company, location, company_url, job_description, date) values(%s, %s, %s, %s, %s, %s, %s, %s);
            """,
                         (id, item['job_url'], tmp['job_title'], tmp['company'], tmp['location'], item['company_url'], tmp['job_description'], item['date'])
            )
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def clean_string(self, input_string):
        cleaned_string = input_string.strip()
        cleaned_string = cleaned_string.replace("\n", " ")
        cleaned_string = " ".join(cleaned_string.split())
        return cleaned_string

    def clean_item(self, item):
        tmp = {}
        tmp['job_title'] = self.clean_string(item['job_title'])
        tmp['company'] = self.clean_string(item['company'])
        tmp['location'] = self.clean_string(item['location'])
        if "%20" in tmp['location']:
            tmp['location'] = tmp['location'].replace("%20", " ")
        tmp['job_description'] = self.clean_string(item['job_description'])
        return tmp
    def check_if_exist(self, id):
        query = "SELECT * FROM linkedin_posts WHERE id = %s"
        self.cur.execute(query, (id,))
        result = self.cur.fetchone()

        if result:
            return True
        else:
            return False

    def string_to_id(self, input_string):
        hash_value = hash(input_string)
        id_value = abs(hash_value)
        return id_value