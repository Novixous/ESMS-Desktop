from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from .base.kobject import KObject

class KSheetsException(Exception):
  pass

class KSheetLabelText(MDLabel):
  klabel = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(KSheetLabelText, self).__init__(**kwargs)

  def on_touch_up(self, touch):
    if not touch.is_mouse_scrolling:
      if self.collide_point(touch.x, touch.y):
        self.klabel.dispatch('on_label_touch')

  pass

class KSheetLabel(BoxLayout):
  ksheet = ObjectProperty(None)
  state = StringProperty('inactive')
  text = StringProperty(None)

  def __init__(self, ksheet=None, text=None, **kwargs):
    self.ksheet = ksheet
    self.text = text
    super(KSheetLabel, self).__init__(**kwargs)
    self.register_event_type('on_label_touch')

  def on_label_touch(self):
    """Called when touching sheet label."""
    if self.state == 'inactive':
      self.ksheet.ksheets.dispatch('on_sheet_switch', self.ksheet)

  def active_sheet(self):
    if self.state == 'inactive':
      self.state = 'active'

  def deactive_sheet(self):
    if self.state == 'active':
      self.state = 'inactive'

  def remove(self):
    self.ksheet.ksheets.dispatch('on_sheet_remove', self.ksheet)

  pass

class KSheetBase(BoxLayout):
  ksheets = ObjectProperty(None)
  previous_sheet = None
  next_sheet = None
  label = ObjectProperty(None)
  text_label = StringProperty(None)

  def __init__(self, ksheets=None, text_label=None, **kwargs):
    self.ksheets = ksheets
    self.text_label = text_label
    self.label = KSheetLabel(ksheet=self, text=self.text_label)
    super(KSheetBase, self).__init__(**kwargs)

  pass

class KSheetsGridLayout(MDGridLayout):
  active_sheet = None

  def __init__(self, **kwargs):
    super(KSheetsGridLayout, self).__init__(**kwargs)

  def change_active(self, sheet):
    if sheet.state == 'active':
      return
    if self.active_sheet is not None:
      self.active_sheet.deactive_sheet()
    self.active_sheet = sheet
    self.active_sheet.active_sheet()

  def add_widget(self, widget, index=0, canvas=None):
    super().add_widget(widget, index=len(self.children))
    if issubclass(widget.__class__, KSheetLabel):
      self.change_active(widget)

  def remove_widget(self, widget):
    if not issubclass(widget.__class__, KSheetLabel):
      raise KSheetsException(
        'KSheetsGridLayout can remove only subclass of KSheetLabel'
      )
    if widget is not None:
      if widget.state == 'active':
        if widget.ksheet.previous_sheet is not None:
          self.change_active(widget.ksheet.previous_sheet.label)
        else:
          if widget.ksheet.next_sheet is not None:
            self.change_active(widget.ksheet.next_sheet.label)
          else:
            self.active_sheet = None
      super().remove_widget(widget)

  pass

class KSheetsBar(BoxLayout):
  scrollview = ObjectProperty(None)
  layout = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(KSheetsBar, self).__init__(**kwargs)

  pass

class KSheetsMain(BoxLayout):

  def __init__(self, **kwargs):
    super(KSheetsMain, self).__init__(**kwargs)

  pass

class KSheets(AnchorLayout, KObject):
  main = ObjectProperty(None)
  bar = ObjectProperty(None)

  def __init__(self, main=None, bar=None, **kwargs):
    self.main = main
    self.bar = bar
    super(KSheets, self).__init__(**kwargs)
    self.first_sheet = None
    self.register_event_type('on_sheet_switch')
    self.register_event_type('on_sheet_remove')

  def on_sheet_switch(self, sheet):
    """Called when switching sheets."""
    self.bar.layout.change_active(sheet.label)
    self.main.clear_widgets()
    self.main.add_widget(sheet)

  def on_sheet_remove(self, sheet):
    """Called when remove a sheet."""
    self.remove_widget(sheet)

  def add_widget(self, widget, index=0, canvas=None):
    if issubclass(widget.__class__, KSheetBase):
      if self.first_sheet is not None:
        self.first_sheet.previous_sheet = widget
      if widget is not None:
        widget.next_sheet = self.first_sheet
      self.first_sheet = widget
      self.bar.layout.add_widget(widget.label)
      self.main.clear_widgets()
      self.main.add_widget(widget)
    else:
      super().add_widget(widget)

  def remove_widget(self, widget):
    if not issubclass(widget.__class__, KSheetBase):
      raise KSheetsException(
        'KSheets can remove only subclass of KSheetBase'
      )
    if widget is not None:
      if widget.previous_sheet is not None:
        widget.previous_sheet.next_sheet = widget.next_sheet
      if widget.next_sheet is not None:
        widget.next_sheet.previous_sheet = widget.previous_sheet
      if widget.previous_sheet is None and widget.next_sheet is None:
        self.first_sheet = None
    self.bar.layout.remove_widget(widget.label)
    self.main.clear_widgets()
    if self.first_sheet is not None:
      self.main.add_widget(self.bar.layout.active_sheet.ksheet)

  pass
