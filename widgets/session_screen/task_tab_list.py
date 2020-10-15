from core.ktab import KMDTabs
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class TaskTabList(FloatLayout, KMDTabs):

  def __init__(self, **kwargs):
    super(TaskTabList, self).__init__(**kwargs)

  def on_tab_switch(self, *args):
    print('Hello tab switch')
