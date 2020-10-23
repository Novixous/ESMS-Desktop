from core.kcard import KMDCardSwipe
from kivy.properties import ObjectProperty, BooleanProperty
import requests

class ShiftItem(KMDCardSwipe):
  shift = ObjectProperty(None)
  is_to_checkin = BooleanProperty(False)

  def __init__(self, **kwargs):
    super(ShiftItem, self).__init__(**kwargs)
    self.is_closing = False

  def close_card(self):
    self.is_closing = True
    super().close_card()

  def on_touch_up(self, touch):
    if self.is_to_checkin:
      if not touch.is_mouse_scrolling:
        if self.collide_point(touch.x, touch.y):
          if self.state == 'closed' and not self.is_closing:
            self.open_card()

  def on_swipe_complete(self, *args):
    self.is_closing = False

  def checkin_shift(self, *args):
    if self.app.token is not None and self.shift is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.put(
        f'{self.app.end_point}/shifts/{self.shift.shid}/checkin',
        headers=headers
      )
      # print('===========\n====checkin shift', response, response.json())
      self.app.shift_id = self.shift.shid
      self.app.queuelist.load_queue()
      self.app.mainscreenmanager.current = 'queue_screen'
