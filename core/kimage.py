from kivy.uix.image import Image
from .base.kobject import KObject

class KImage(Image, KObject):

  def __init__(self, **kwargs):
    super(KImage, self).__init__(**kwargs)

  pass
