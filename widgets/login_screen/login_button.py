from core.kbutton import KMDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
import requests

class LoginButton(KMDRectangleFlatButton):

  def __init__(self, **kwargs):
    super(LoginButton, self).__init__(**kwargs)
    self.emp_code_inp = ObjectProperty(None)
    self.emp_pass_inp = ObjectProperty(None)

  def action(self, *args):
    self.login()

  def login(self, *args):
    employeeCode = self.emp_code_inp.text
    password = self.emp_pass_inp.text
    response = requests.post(
      f'{self.app.end_point}/login',
      data={'employeeCode': employeeCode, 'password': password}
    )
    json_respone = response.json()
    loginSuccess = json_respone['status']

    if not loginSuccess:
      Snackbar(text='Login FAILED!', duration=1).show()
    else:
      self.app.token = json_respone['token']
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response2 = requests.get(
        f'{self.app.end_point}/shifts/active-shift',
        headers=headers
      )
      json_respone2 = response2.json()
      active_shifts = json_respone2['message']
      if active_shifts is not None and len(active_shifts) > 0:
        self.app.shift_id = active_shifts[0]['id']
        self.app.counter_id = active_shifts[0]['counterId']
        self.app.queuelist.load_queue()
        Window.maximize()
        self.app.mainscreenmanager.current = 'queue_screen'
