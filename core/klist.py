from kivymd.uix.list import MDList, OneLineAvatarIconListItem
from .base.kobject import KObject

class KMDList(MDList, KObject):

  def __init__(self, **kwargs):
    super(KMDList, self).__init__(**kwargs)

  pass

class KOneLineAvatarIconListItem(OneLineAvatarIconListItem, KObject):

  def __init__(self, **kwargs):
    super(KOneLineAvatarIconListItem, self).__init__(**kwargs)

  pass
