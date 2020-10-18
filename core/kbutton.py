from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from .base.kobject import KObject

class KMDRectangleFlatButton(MDRectangleFlatButton, KObject):

  def __init__(self, **kwargs):
    super(KMDRectangleFlatButton, self).__init__(**kwargs)
    self.bind(on_release=self.action)

  def action(self, *args):
    pass

  pass

class KMDIconButton(MDIconButton, KObject):

  def __init__(self, **kwargs):
    super(KMDIconButton, self).__init__(**kwargs)
    self.bind(on_release=self.action)

  def action(self, *args):
    pass

  pass
