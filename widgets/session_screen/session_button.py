from core.kbutton import KMDFillRoundFlatIconButton

class CompleteSessionButton(KMDFillRoundFlatIconButton):

  def __init__(self, **kwargs):
    super(CompleteSessionButton, self).__init__(**kwargs)

  def action(self, *args):
    self.app.tasksheets.clear_sheets()
    self.app.cameraimage.close_camera()
    self.app.emotion_color = '#888888'
