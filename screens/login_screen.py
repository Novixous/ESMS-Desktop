from kivy.uix.widget import Widget
from kivymd.uix.snackbar import Snackbar
import requests

class LoginScreen(Widget):
  def login(self, username, password):
    response = requests.post('http://localhost:4000/login', data={'username': username, 'password': password})
    jsonResponse = response.json()
    loginSuccess = jsonResponse['status']
    if not loginSuccess:
      Snackbar(text="Login failed!", duration=1).show()
    return loginSuccess
