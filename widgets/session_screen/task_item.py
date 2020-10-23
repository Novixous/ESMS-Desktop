from core.klist import KOneLineAvatarIconListItem
from kivy.properties import ObjectProperty
from .task_sheet_base import TaskSheetBase
import requests

class SessionTask():

  def __init__(self, stid=None, name=None, code=None):
    self.stid = stid
    self.name = name
    self.code = code

class TaskItem(KOneLineAvatarIconListItem):
  task = ObjectProperty(None)

  def __init__(self, **kwargs):
    self._no_ripple_effect = True
    super(TaskItem, self).__init__(**kwargs)

  def add_task_to_session(self):
    if self.app.token is not None and self.app.session_id is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.post(
        f'{self.app.end_point}/session-tasks/assign',
        json={'sessionId': self.app.session_id, 'taskId': self.task.tid},
        headers=headers
      )
      json_respone = response.json()
      data = json_respone['message']
      # print('===========\n====add session task', response, response.json())

      self.app.tasksheets.add_sheet(
        TaskSheetBase(
          session_task=SessionTask(
            stid=data['id'],
            name=self.task.name,
            code=self.task.code
          ),
          ksheets=self.app.tasksheets,
          text_label=self.task.name
        )
      )
