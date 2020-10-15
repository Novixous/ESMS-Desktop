from core.ktab import KMDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

class TaskTab(FloatLayout, KMDTabsBase):
  text = StringProperty(None)

  def __init__(self, **kwargs):
    super(TaskTab, self).__init__(**kwargs)
