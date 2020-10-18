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

import widgets.widget_list

class ESMSApp(MDApp):
  token = StringProperty(None)
  counter_id = NumericProperty(None)
  session_id = NumericProperty(None)
  emotion_color = StringProperty('#000000')
  task_list = ObjectProperty(None)
  end_point = StringProperty('http://localhost:4000')

  def __init__(self, **kwargs):
    super(ESMSApp, self).__init__(**kwargs)

  def build(self):
    self.theme_cls.primary_palette = 'BlueGray'
    layout = Builder.load_file(resource_path('main.kv'))
    return layout

  def set_emotion_color(self, color):
    self.emotion_color = color

  pass

def main():
  ESMSApp().run()

if __name__ == '__main__':
  main()
