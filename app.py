import kivy
kivy.require('1.11.1')

from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '340')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from PathUtil import resource_path
from widgets.session_screen.checkout_dialog import CheckoutDialog
from widgets.session_screen.session_result_dialog import SessionResultDialog, SessionResultContent
from widgets.session_screen.shift_summary import ShiftSummaryDialog, ShiftSummaryContent
from widgets.checkout_button import CheckoutButton

import widgets.widget_list
import requests
from kivy.core.window import Window

class ESMSApp(MDApp):
  token = None
  counter_id = None
  shift_id = None
  session_id = None
  emotion_color = StringProperty('#888888')
  end_point = 'http://api.esms-team.site'
  checkout_dialog = None
  session_result_dialog = None
  session_result_content = None
  session_result_map = ObjectProperty(None)
  shift_summary_dialog = None
  shift_summary_content = None
  shift_summary_map = ObjectProperty(None)
  login_window = None
  full_screen_window = None

  def __init__(self, **kwargs):
    super(ESMSApp, self).__init__(**kwargs)
    Window.bind(on_request_close=self.on_exit_window)

  def build(self):
    self.theme_cls.primary_palette = 'BlueGray'
    layout = Builder.load_file(resource_path('main.kv'))
    self.checkout_dialog = CheckoutDialog(
      title='CHECK OUT SHIFT',
      text='Do you want to check out this shift and logout?',
      buttons=[
        CheckoutButton()
      ]
    )

    self.shift_summary_content = ShiftSummaryContent()
    self.shift_summary_dialog = ShiftSummaryDialog(
      title='SHIFT SUMMARY',
      type='custom',
      content_cls=self.shift_summary_content,
      buttons=[
        CheckoutButton()
      ]
    )
    self.shift_summary_dialog.width = self.shift_summary_dialog.content_cls.width + 50

    self.session_result_content = SessionResultContent()
    self.session_result_dialog = SessionResultDialog(
      title='SESSION RESULT',
      type='custom',
      content_cls=self.session_result_content
    )
    self.session_result_dialog.width = self.session_result_dialog.content_cls.width + 50
    self.login_window = {
      'width': Window.width,
      'height': Window.height,
      'top': Window.top,
      'left': Window.left
    }
    return layout

  def on_exit_window(self, *args):
    if (
      self.mainscreenmanager.current != 'login_screen'
      and self.mainscreenmanager.current != 'checkin_screen'
    ):
      if not self.checkout_dialog._window:
        self.checkout_dialog.open()
      return True

  def set_emotion_color(self, color):
    self.emotion_color = color

  def ms_to_str(self, ms, call_count=1):
    if ms < 1000:
      return str(ms) + f' ms'
    if ms < 60000:
      secs = ms // 1000
      call_count += 1
      return str(secs) + f' sec{"" if secs == 1 else "s"}'
    if ms < 3600000:
      mins = ms // 60000
      call_count += 1
      return str(mins) + f' min{"" if mins == 1 else "s"} ' + (
        self.ms_to_str(ms % 60000, call_count)
      )
    hours = ms // 3600000
    call_count += 1
    return str(hours) + f' hour{"" if hours == 1 else "s"} ' + (
      self.ms_to_str(ms % 3600000, call_count)
    )

  def open_shift_summary(self, *args):
    if self.token is not None and self.shift_id is not None:
      bearer_token = f'Bearer {self.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.end_point}/shifts/{self.shift_id}/summary',
        headers=headers
      )
      print('===========\n====get shift summary', response, response.json())
      json_respone = response.json()
      data = json_respone['message']
      self.shift_summary_map = data
      self.shift_summary_dialog.open()

  pass

def main():
  ESMSApp().run()

if __name__ == '__main__':
  main()
