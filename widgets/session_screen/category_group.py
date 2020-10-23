from core.kexpansionpanel import KMDExpansionPanel
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine
from kivymd.uix.list import MDList
from kivy.properties import ObjectProperty
from .task_item import TaskItem
import requests

class Task():

  def __init__(self, tid=None, name=None, code=None):
    self.tid = tid
    self.name = name
    self.code = code

class CategoryGroup(KMDExpansionPanel):
  category = ObjectProperty(None)

  def __init__(self, **kwargs):
    self.icon = 'assets/category.jpg'
    self.panel_cls = MDExpansionPanelOneLine()
    super(CategoryGroup, self).__init__(**kwargs)

  def load_tasks(self):
    self.panel_cls.text = self.category.name
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.app.end_point}/categories/{self.category.cid}/tasks',
        headers=headers
      )
      # print('===========\n====get tasks by category', response, response.json())
      json_response = response.json()
      data = json_response['message']
      task_list = MDList()
      for d in data:
        t = Task(
          tid=d['id'],
          name=d['name'],
          code=d['code']
        )
        task_list.add_widget(
          TaskItem(
            task=t,
            skip_self_register=True
          )
        )
      self.content = task_list
