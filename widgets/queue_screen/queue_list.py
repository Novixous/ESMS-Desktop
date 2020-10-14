from core.klist import KMDList
from kivy.properties import ObjectProperty
from widgets.queue_screen.queue_item import QueueItem

class QueueList(KMDList):
  active_item = ObjectProperty(None)

  def load_queue(self):
    for i in range(20):
      self.add_widget(
        QueueItem(text=f"Customer {i}", skip_self_register=True)
      )
