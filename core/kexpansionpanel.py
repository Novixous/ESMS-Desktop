from kivymd.uix.expansionpanel import MDExpansionPanel
from .base.kobject import KObject

class KMDExpansionPanel(MDExpansionPanel, KObject):

  def __init__(self, **kwargs):
    super(KMDExpansionPanel, self).__init__(**kwargs)

  pass
