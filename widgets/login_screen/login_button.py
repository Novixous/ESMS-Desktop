from core.kbutton import KMDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
from kivy.clock import Clock
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
      self.app.queuelist.load_queue()
      Window.maximize()
      self.app.mainscreenmanager.current = 'queue_screen'

    # Window.maximize()

    # self.app.queuelist.load_queue()
    # self.app.mainscreenmanager.current = 'queue_screen'

    # self.app.tasklist.load_task()
    # self.app.mainscreenmanager.current = 'session_screen'
    
    # def open_session_camera(interval):
    #   self.app.cameraimage.open_camera()
    # Clock.schedule_once(open_session_camera, 0)
