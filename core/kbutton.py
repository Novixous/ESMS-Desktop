from kivymd.uix.button import MDRectangleFlatButton
from .base.kobject import KObject

class KMDRectangleFlatButton(MDRectangleFlatButton, KObject):

  def __init__(self, **kwargs):
    super(KMDRectangleFlatButton, self).__init__(**kwargs)
    self.bind(on_press=self.action)

  def action(self, *args):
    pass

  pass
