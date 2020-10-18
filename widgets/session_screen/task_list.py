from core.klist import KMDList
from widgets.session_screen.task_item import TaskItem
import requests

class Category():

  def __init__(self, cid=None, name=None, **kwargs):
    self.cid = cid
    self.name = name

class Task():

  def __init__(self, tid=None, name=None, code=None, **kwargs):
    self.tid = tid
    self.name = name
    self.code = code

class TaskList(KMDList):

  def __init__(self, **kwargs):
    super(TaskList, self).__init__(**kwargs)

  def load_task(self):
    if self.app.token is not None and self.app.counter_id is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.app.end_point}/categories/counters/{self.app.counter_id}',
        headers=headers
      )
      json_respone = response.json()
      categories = []
      data = json_respone['message']
      for d in data:
        cat = Category(
          cid=d['id'],
          name=d['categoryName']
        )
        categories.append(cat)
      tasks = []
      if len(categories) > 0:
        for c in categories:    
          res2 = requests.get(
            f'{self.app.end_point}/task-type/{c.cid}',
            headers=headers
          )
          json_res2 = res2.json()
          data2 = json_res2['message']
          for d2 in data2:
            tk = Task(
              tid=d2['id'],
              name=d2['typeName'],
              code=d2['taskCode']
            )
            tasks.append(tk)
        if len(tasks) > 0:
          for t in tasks:
            self.add_widget(
              TaskItem(
                task=t,
                skip_self_register=True
              )
            )
    else:
      for t in range(20):
        tno = f'000{t}'
        self.add_widget(
          TaskItem(
            task=Task(
              tid=t,
              name=f'Task number {tno[(len(tno) - 3):]}',
              code=f'T{tno[(len(tno) - 3):]}'
            ),
            skip_self_register=True
          )
        )

  def clear_task(self):
    self.clear_widgets()
