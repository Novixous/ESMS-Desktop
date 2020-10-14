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

  def remove_from_queue(self, item):
    self.remove_widget(item)

  def clear_queue(self):
    while len(self.children) > 0:
      self.remove_widget(self.children[0])
