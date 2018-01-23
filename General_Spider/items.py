# This is the items that will be saved to JSON files

from scrapy.item import Item, Field

class FlexibleItem(Item):
# The setitem function is called whenever a spider generates a new item
    def __setitem__(self, key, value):
        if key not in self.fields: #the self.fields contains the already existed items. So, we check if the inserted key exists in the fields or not.
            self.fields[key] = Field()
        self._values[key] = value
