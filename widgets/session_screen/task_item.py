from core.klist import KOneLineAvatarIconListItem
from kivy.properties import ObjectProperty
from core.ksheet import KSheetBase

class TaskItem(KOneLineAvatarIconListItem):
  task = ObjectProperty(None)

  def __init__(self, **kwargs):
    self._no_ripple_effect = True
    super(TaskItem, self).__init__(**kwargs)

  def add_task_to_session(self):
    print('SESSIONIDDDD', self.app.session_id)
    print('TASKIDDDD', self.task.tid)
    self.app.tasksheets.add_widget(
      KSheetBase(
        ksheets=self.app.tasksheets,
        text_label=self.task.name
      )
    )
