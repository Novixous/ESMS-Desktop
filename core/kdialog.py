from kivymd.uix.dialog import MDDialog
from .base.kobject import KObject

class KMDDialog(MDDialog, KObject):

  def __init__(self, **kwargs):
    super(KMDDialog, self).__init__(**kwargs)

  pass
