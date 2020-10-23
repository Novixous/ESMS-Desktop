from kivy.uix.boxlayout import BoxLayout
from .base.kobject import KObject

class KBoxLayout(BoxLayout, KObject):

  def __init__(self, **kwargs):
    super(KBoxLayout, self).__init__(**kwargs)

  pass
