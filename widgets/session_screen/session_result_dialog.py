from core.kdialog import KMDDialog
from core.kboxlayout import KBoxLayout

class SessionResultDialog(KMDDialog):

  def __init__(self, **kwargs):
    super(SessionResultDialog, self).__init__(skip_self_register=True, **kwargs)

class SessionResultContent(KBoxLayout):
  session_result = None

  def __init__(self, **kwargs):
    super(SessionResultContent, self).__init__(skip_self_register=True, **kwargs)
