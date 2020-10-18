from core.kdialog import KMDDialog

class WarningDialog(KMDDialog):

  def __init__(self, **kwargs):
    super(WarningDialog, self).__init__(skip_self_register=True, **kwargs)
