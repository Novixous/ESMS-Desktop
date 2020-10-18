from core.klist import KMDList
from .category_group import CategoryGroup
import requests

class Category():

  def __init__(self, cid=None, name=None):
    self.cid = cid
    self.name = name

class CategoryList(KMDList):

  def __init__(self, **kwargs):
    super(CategoryList, self).__init__(**kwargs)

  def load_categories(self):
    if self.app.token is not None and self.app.counter_id is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.app.end_point}/categories/counters/{self.app.counter_id}',
        headers=headers
      )
      json_respone = response.json()
      data = json_respone['message']
      for d in data:
        cat = Category(
          cid=d['id'],
          name=d['categoryName']
        )
        cat_group = CategoryGroup(
          category=cat,
          skip_self_register=True
        )
        cat_group.load_tasks()
        self.add_widget(cat_group)

  def clear_categories(self):
    self.clear_widgets()
