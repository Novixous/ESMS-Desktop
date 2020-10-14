from core.kbutton import KMDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
import requests

class LoginButton(KMDRectangleFlatButton):
  emp_code_inp = ObjectProperty()
  emp_pass_inp = ObjectProperty()

  def action(self, *args):
    # employeeCode = self.emp_code_inp.text
    # password = self.emp_pass_inp.text
    # response = requests.post('http://10.1.129.103:4000/login', data={'employeeCode': employeeCode, 'password': password})
    # jsonResponse = response.json()
    # loginSuccess = jsonResponse['status']

    # if not loginSuccess:
    #   Snackbar(text='Login FAILED!', duration=1).show()
    # else:
    #   self.app.queuelist.load_queue()
    #   self.app.mainscreenmanager.current = 'session_screen'
    #   Window.maximize()
    self.app.queuelist.load_queue()
    self.app.mainscreenmanager.current = 'queue_screen'
    Window.maximize()
