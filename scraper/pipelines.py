import json
import csv
import os
from itemadapter import ItemAdapter
from utils.data_cleaner import clean_data
from config import OUTPUT_FOLDER

class ScraperPipeline:
    def __init__(self):
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        self.json_file = open(os.path.join(OUTPUT_FOLDER, 'output.json'), 'w')
        self.csv_file = open(os.path.join(OUTPUT_FOLDER, 'output.csv'), 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['name', 'brand', 'price', 'sizes', 'color', 'description', 'details', 'quantity'])

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        clean_data(adapter)

        line = json.dumps(adapter.asdict()) + "\n"
        self.json_file.write(line)

        self.csv_writer.writerow([
            adapter['name'],
            adapter['brand'],
            adapter['price'],
            ','.join(adapter['sizes']),
            adapter['color'],
            adapter['description'],
            adapter['details'],
            adapter['quantity']
        ])

        return item

    def close_spider(self, spider):
        self.json_file.close()
        self.csv_file.close()
