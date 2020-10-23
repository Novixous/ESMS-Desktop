from core.ksheet import KSheetBase
from kivy.properties import ObjectProperty
import requests

class TaskSheetBase(KSheetBase):
  session_task = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(TaskSheetBase, self).__init__(**kwargs)

  def complete_session_task(self):
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.put(
        f'{self.app.end_point}/session-tasks/{self.session_task.stid}/status',
        json={'statusId': 3},
        headers=headers
      )
      # print('===========\n====complete session task', response, response.json())
