from core.kbutton import KMDIconButton
from kivy.properties import NumericProperty
import requests

class PickQueueButton(KMDIconButton):
  queue_id = NumericProperty(None)

  def action(self, *args):
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.app.end_point}/counters',
        headers=headers
      )
      json_respone = response.json()
      data = json_respone['message']
      counterId = data['counterId']
      self.app.counter_id = counterId

      res2 = requests.post(
        f'{self.app.end_point}/queues/assign',
        headers=headers,
        data={'counterId':counterId,'queueId':self.queue_id}
      )

      res3 = requests.post(
        f'{self.app.end_point}/sessions',
        headers=headers
      )
      json_res3 = res3.json()
      data3 = json_res3['message']
      self.app.session_id = data3['id']

      self.app.tasklist.load_task()
      self.app.mainscreenmanager.current = 'session_screen'
      self.app.cameraimage.open_camera()
