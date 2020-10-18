from core.kbutton import KMDRectangleFlatButton

class CompleteSessionButton(KMDRectangleFlatButton):

  def __init__(self, **kwargs):
    super(CompleteSessionButton, self).__init__(**kwargs)

  def action(self, *args):
    self.app.queuelist.clear_queue()
    self.app.cameraimage.close_camera()
    self.app.queuelist.load_queue()
    self.app.mainscreenmanager.current = 'queue_screen'
