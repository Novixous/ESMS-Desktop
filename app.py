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
from widgets.checkout_button import CheckoutButton

import widgets.widget_list
from kivy.core.window import Window

class ESMSApp(MDApp):
  token = None
  counter_id = None
  shift_id = None
  session_id = None
  emotion_color = StringProperty('#888888')
  end_point = 'http://localhost:4000'
  checkout_dialog = None
  session_result_dialog = None
  session_result_content = None
  session_result_map = ObjectProperty(None)
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

  pass

def main():
  ESMSApp().run()

if __name__ == '__main__':
  main()
