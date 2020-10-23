from core.kdialog import KMDDialog
from core.kboxlayout import KBoxLayout

class ShiftSummaryDialog(KMDDialog):

  def __init__(self, **kwargs):
    super(ShiftSummaryDialog, self).__init__(skip_self_register=True, **kwargs)

class ShiftSummaryContent(KBoxLayout):

  def __init__(self, **kwargs):
    super(ShiftSummaryContent, self).__init__(skip_self_register=True, **kwargs)
