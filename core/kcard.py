from kivymd.uix.card import MDCardSwipe
from .base.kobject import KObject

class KMDCardSwipe(MDCardSwipe, KObject):

  def __init__(self, **kwargs):
    super(KMDCardSwipe, self).__init__(**kwargs)

  pass
