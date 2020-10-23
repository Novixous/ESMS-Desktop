from core.klist import KMDList
from kivy.properties import ObjectProperty
from widgets.checkin_screen.shift_item import ShiftItem
import requests

class ActiveShiftList(KMDList):

  def __init__(self, **kwargs):
    super(ActiveShiftList, self).__init__(**kwargs)

  def add_shift(self, shift_item):
    self.add_widget(shift_item)

  def clear_shift(self):
    self.clear_widgets()
