from core.klist import KMDList
from kivy.properties import ObjectProperty
from widgets.queue_screen.queue_item import QueueItem
import requests

class Queue():

  def __init__(self, qid=None, qno=None, qcat=None, **kwargs):
    self.qid = qid
    self.qno = qno
    self.qcat = qcat

class QueueList(KMDList):
  active_item = ObjectProperty(None)

  def load_queue(self):
    self.app.tasklist.clear_task()
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.app.end_point}/queues',
        headers=headers
      )
      json_respone = response.json()
      queues = []
      data = json_respone['message']
      for d in data:
        queue = Queue(
          qid=d['id'],
          qno=d['number'],
          qcat=d['Category']['categoryName']
        )
        queues.append(queue)
      if len(queues) > 0:
        for q in queues:
          qno = f'0000{q.qno}'
          self.add_widget(
            QueueItem(
              queue_id=q.qid,
              queue_no=qno[(len(qno) - 4):],
              queue_cat=f'{q.qcat}',
              skip_self_register=True
            )
          )

  def remove_from_queue(self, item):
    self.remove_widget(item)

  def clear_queue(self):
    while len(self.children) > 0:
      self.remove_widget(self.children[0])
