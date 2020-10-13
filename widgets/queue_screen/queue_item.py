from core.kcard import KMDCardSwipe
from kivy.properties import StringProperty

class QueueItem(KMDCardSwipe):
  text = StringProperty()

  def action(self, *args):
    print('Hello swipe')
    self.app.queuelist.remove_widget(self)
