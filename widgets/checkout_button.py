from core.kbutton import KMDFlatButton
from kivy.core.window import Window
from kivy.clock import Clock
import requests

class CheckoutButton(KMDFlatButton):

  def __init__(self, **kwargs):
    super(CheckoutButton, self).__init__(**kwargs)

  def on_touch_up(self, touch):
    if not touch.is_mouse_scrolling:
      if self.collide_point(touch.x, touch.y):
        if self.app.token is not None and self.app.shift_id is not None:
          bearer_token = f'Bearer {self.app.token}'
          headers = {'Authorization': bearer_token}
          response = requests.put(
            f'{self.app.end_point}/shifts/{self.app.shift_id}/checkout',
            headers=headers
          )
          # print('===========\n====checkout shift', response, response.json())
        self.app.counter_id = None
        self.app.shift_id = None
        self.app.token = None
        self.app.mainscreenmanager.current = 'login_screen'
        if self.app.login_window is not None:
          def resize_window(*args):
            Window.size = (self.app.login_window['width'], self.app.login_window['height'])
            Window.top = self.app.login_window['top']
            Window.left = self.app.login_window['left']
          Clock.schedule_once(resize_window, 0.1)
