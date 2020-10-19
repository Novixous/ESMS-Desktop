import kivy
kivy.require('1.11.1')

from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '340')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from PathUtil import resource_path
from widgets.session_screen.checkout_dialog import CheckoutDialog
from kivymd.uix.button import MDFlatButton

import widgets.widget_list
from kivy.core.window import Window
Window.clearcolor = (0, 0, 0, 1)

class ESMSApp(MDApp):
  token = StringProperty(None)
  counter_id = NumericProperty(None)
  shift_id = NumericProperty(None)
  session_id = NumericProperty(None)
  emotion_color = StringProperty('#000000')
  end_point = StringProperty('http://localhost:4000')

  def __init__(self, **kwargs):
    super(ESMSApp, self).__init__(**kwargs)
    Window.bind(on_request_close=self.on_exit_window)

  def build(self):
    self.theme_cls.primary_palette = 'BlueGray'
    layout = Builder.load_file(resource_path('main.kv'))
    self.do_exit_btn = MDFlatButton(
      text='CHECK OUT',
      text_color=self.theme_cls.primary_color
    )
    self.do_exit_btn.bind(on_press=self.do_exit_window)
    self.checkout_dialog = CheckoutDialog(
      title='CHECK OUT SHIFT',
      text='Do you want to check out this shift and logout?',
      buttons=[
        self.do_exit_btn
      ]
    )
    return layout

  def on_exit_window(self, *args):
    if self.mainscreenmanager.current != 'login_screen':
      if not self.checkout_dialog._window:
        self.checkout_dialog.open()
      return True

  def do_exit_window(self, *args):
    Window.unbind(on_request_close=self.on_exit_window)
    Window.close()

  def set_emotion_color(self, color):
    self.emotion_color = color

  pass

def main():
  ESMSApp().run()

if __name__ == '__main__':
  main()
