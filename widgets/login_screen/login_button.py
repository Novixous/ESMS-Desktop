from core.kbutton import KMDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
import requests

class LoginButton(KMDRectangleFlatButton):
  emp_code_inp = ObjectProperty()
  emp_pass_inp = ObjectProperty()

  def action(self, *args):
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
      self.app.queuelist.load_queue()
      self.app.mainscreenmanager.current = 'queue_screen'
      Window.maximize()
    # self.app.queuelist.load_queue()
    # self.app.mainscreenmanager.current = 'queue_screen'
    # Window.maximize()
