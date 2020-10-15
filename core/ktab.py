from kivymd.uix.tab import MDTabs, MDTabsBase
from .base.kobject import KObject

class KMDTabs(MDTabs, KObject):

  def __init__(self, **kwargs):
    super(KMDTabs, self).__init__(**kwargs)

  pass

class KMDTabsBase(MDTabsBase, KObject):

  def __init__(self, **kwargs):
    super(KMDTabsBase, self).__init__(**kwargs)

  pass
