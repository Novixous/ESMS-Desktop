from core.kbutton import KMDRectangleFlatButton

class CompleteSessionButton(KMDRectangleFlatButton):

  def action(self, *args):
    print('Hello CompleteSessionButton')
    self.app.queuelist.clear_queue()
    self.app.cameraimage.close_camera()
    self.app.queuelist.load_queue()
    self.app.mainscreenmanager.current = 'queue_screen'
