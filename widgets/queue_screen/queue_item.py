from core.kcard import KMDCardSwipe
from kivy.properties import ObjectProperty

class QueueItem(KMDCardSwipe):
  queue = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(QueueItem, self).__init__(**kwargs)
    self.is_closing = False

  def close_card(self):
    self.is_closing = True
    super().close_card()

  def on_touch_up(self, touch):
    if not touch.is_mouse_scrolling:
      if self.collide_point(touch.x, touch.y):
        if self.state == 'closed' and not self.is_closing:
          if self.app.queuelist.active_item is not None:
            self.app.queuelist.active_item.close_card()
          self.app.queuelist.active_item = self
          self.app.queuelist.active_item.open_card()

  def on_swipe_complete(self, *args):
    self.is_closing = False
