from core.klist import KMDList
from kivy.properties import ObjectProperty
from widgets.queue_screen.queue_item import QueueItem
import requests

class Queue():

  def __init__(self, qid=None, number=None, category=None):
    self.qid = qid
    self.number = number
    self.category = category

class QueueList(KMDList):
  active_item = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(QueueList, self).__init__(**kwargs)

  def load_queue(self):
    self.app.categorylist.clear_categories()
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.app.end_point}/queues',
        headers=headers
      )
      # print('===========\n====get queue', response, response.json())
      json_respone = response.json()
      data = json_respone['message']
      for d in data:
        qno = d['number']
        qno = f'0000{qno}'
        queue = Queue(
          qid=d['id'],
          number=qno[(len(qno) - 4):],
          category=d['Category']['categoryName']
        )
        self.add_widget(
          QueueItem(
            queue=queue,
            skip_self_register=True
          )
        )

  def remove_from_queue(self, item):
    self.remove_widget(item)

  def clear_queue(self):
    self.clear_widgets()
