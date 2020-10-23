from core.ksheet import KSheets
import requests

class TaskSheets(KSheets):

  def __init__(self, **kwargs):
    super(TaskSheets, self).__init__(**kwargs)

  def remove_session_task(self, session_task_id):
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.delete(
        f'{self.app.end_point}/session-tasks/{session_task_id}',
        headers=headers
      )
      # print('===========\n====remove session task', response, response.json())
