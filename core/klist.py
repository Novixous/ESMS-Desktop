from kivymd.uix.list import MDList
from .base.kobject import KObject

class KMDList(MDList, KObject):

  def __init__(self, **kwargs):
    super(KMDList, self).__init__(**kwargs)

  pass
