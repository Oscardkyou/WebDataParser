import re

def clean_data(item):
    for field in item.fields:
        if field in item:
            if isinstance(item[field], str):
                item[field] = item[field].strip()
            elif isinstance(item[field], list):
                item[field] = [i.strip() for i in item[field] if i.strip()]

    if 'price' in item:
        item['price'] = re.sub(r'[^\d.]', '', item['price'])

    if 'sizes' in item and isinstance(item['sizes'], str):
        item['sizes'] = [size.strip() for size in item['sizes'].split(',')]

    return item
