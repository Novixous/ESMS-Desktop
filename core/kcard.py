from kivymd.uix.card import MDCardSwipe
from .base.kobject import KObject

class KMDCardSwipe(MDCardSwipe, KObject):

  def __init__(self, **kwargs):
    super(KMDCardSwipe, self).__init__(**kwargs)
    self.bind(on_swipe_complete=self.action)

  def action(self, *args):
    pass

  pass
