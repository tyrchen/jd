# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.directory
employees = db['employees']

special_employees = {
    'tchen': 'Cliff Guo',
}


class MongoPipeline(object):
    def add_to_collection(self, col, employee):
        uid = employee['uid']
        em = col.find_one({'uid': uid})
        if not em:
            col.insert(employee)
        else:
            col.update({'uid': uid}, employee)

    def process_employee(self, item):
        employee = dict(item)
        if 'uid' in special_employees:
            employee['original_manager'] = employee['manager']
            employee['manager'] = special_employees[employee['uid']]

        return employee

    def process_item(self, item, spider):
        employee = self.process_employee(item)
        self.add_to_collection(employees, employee)
        self.add_to_collection(db['snapshot%s' % datetime.today().strftime('%Y%m%d')], employee)
        return item
