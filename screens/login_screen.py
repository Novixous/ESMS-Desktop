from kivy.uix.widget import Widget
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
from kivy.app import App
import requests

class LoginScreen(Widget):
  def login(self, employeeCode, password):
    response = requests.post('http://localhost:4000/login', data={'employeeCode': employeeCode, 'password': password})
    jsonResponse = response.json()
    loginSuccess = jsonResponse['status']
    print('MANAGER', App.get_running_app().screen_manager)
    if not loginSuccess:
      Snackbar(text="Login failed!", duration=1).show()
    else:
      Window.maximize()
    return loginSuccess
