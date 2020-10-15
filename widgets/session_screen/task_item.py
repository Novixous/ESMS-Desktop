from core.klist import KOneLineAvatarIconListItem
from kivy.properties import ObjectProperty

class TaskItem(KOneLineAvatarIconListItem):
  task = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(TaskItem, self).__init__(**kwargs)

  def add_task_to_session(self):
    print('Hello add task', self.task.name)
