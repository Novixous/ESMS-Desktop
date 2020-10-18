from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from .base.kobject import KObject

class KScreenManager(ScreenManager, KObject):

  def __init__(self, **kwargs):
    super(KScreenManager, self).__init__(**kwargs)
    self.transition = NoTransition()

  pass

class KScreen(Screen, KObject):

  def __init__(self, **kwargs):
    super(KScreen, self).__init__(**kwargs)

  pass
