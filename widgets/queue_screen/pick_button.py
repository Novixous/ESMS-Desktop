from core.kbutton import KMDIconButton
from kivy.properties import NumericProperty
import requests

class PickQueueButton(KMDIconButton):

  def __init__(self, **kwargs):
    super(PickQueueButton, self).__init__(**kwargs)
    self.queue_id = NumericProperty(None)

  def action(self, *args):
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      print('self.app.counter_id:', self.app.counter_id)
      if self.app.counter_id is None:
        response = requests.get(
          f'{self.app.end_point}/counters',
          headers=headers
        )
        json_respone = response.json()
        data = json_respone['message']
        self.app.counter_id = data['counterId']

      res2 = requests.post(
        f'{self.app.end_point}/queues/assign',
        headers=headers,
        data={'counterId':self.app.counter_id,'queueId':self.queue_id}
      )

      res3 = requests.post(
        f'{self.app.end_point}/sessions',
        headers=headers
      )
      json_res3 = res3.json()
      data3 = json_res3['message']
      self.app.session_id = data3['id']

      self.app.categorylist.load_categories()
      self.app.mainscreenmanager.current = 'session_screen'
      self.app.cameraimage.open_camera()
