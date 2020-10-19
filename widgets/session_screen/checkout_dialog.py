from core.kdialog import KMDDialog

class CheckoutDialog(KMDDialog):

  def __init__(self, **kwargs):
    super(CheckoutDialog, self).__init__(skip_self_register=True, **kwargs)
