from kivymd.uix.button import (
  MDRectangleFlatButton,
  MDRectangleFlatIconButton,
  MDFillRoundFlatIconButton,
  MDIconButton,
  MDFlatButton,
)
from kivy.clock import Clock
from .base.kobject import KObject

class KMDRectangleFlatButton(MDRectangleFlatButton, KObject):

  def __init__(self, **kwargs):
    super(KMDRectangleFlatButton, self).__init__(**kwargs)
    self.bind(on_release=self.call_action)

  def call_action(self, *args):
    Clock.schedule_once(self.action, 0.2)

  def action(self, *args):
    pass

  pass

class KMDRectangleFlatIconButton(MDRectangleFlatIconButton, KObject):

  def __init__(self, **kwargs):
    super(KMDRectangleFlatIconButton, self).__init__(**kwargs)
    self.bind(on_release=self.call_action)

  def call_action(self, *args):
    Clock.schedule_once(self.action, 0.2)

  def action(self, *args):
    pass

  pass

class KMDFillRoundFlatIconButton(MDFillRoundFlatIconButton, KObject):

  def __init__(self, **kwargs):
    super(KMDFillRoundFlatIconButton, self).__init__(**kwargs)
    self.bind(on_release=self.call_action)

  def call_action(self, *args):
    Clock.schedule_once(self.action, 0.2)

  def action(self, *args):
    pass

  pass

class KMDIconButton(MDIconButton, KObject):

  def __init__(self, **kwargs):
    super(KMDIconButton, self).__init__(**kwargs)
    self.bind(on_release=self.call_action)

  def call_action(self, *args):
    Clock.schedule_once(self.action, 0.2)

  def action(self, *args):
    pass

  pass

class KMDFlatButton(MDFlatButton, KObject):

  def __init__(self, **kwargs):
    super(KMDFlatButton, self).__init__(**kwargs)

  pass
