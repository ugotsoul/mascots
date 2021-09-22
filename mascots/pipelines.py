import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MascotImagesPipeline(ImagesPipeline):
    # TODO: write a dynamic image path based on year and if the image is local (bool)
    def file_path(self, request, response=None, info=None, *, item=None):
        name = item['name'].lower().replace('/','&')
        folder = 'local' if item['is_local'] else 'corporate'
        year = item['year']

        return f'{year}/{folder}/{name}.jpg' 

    # def item_completed(self, results, item, info):
    #     adapter = ItemAdapter(item)

    #     if results: 
    #         _, image_data = results[0]
    #         item['image_path'] = f"images/{image_data['path']}"
        
    #     return item


class DuplicatesPipeline:

    def __init__(self):
        self.name_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.name_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.name_seen.add(adapter['name'])
            return item
