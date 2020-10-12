from kivy.app import App

class KObject:
  def __init__(self, **kwargs):
    cls = f'{self.__class__.__name__}'.lower()
    self.kid = cls
    esmsApp = App.get_running_app()

    setattr(esmsApp, cls, self)
    setattr(self, 'app', esmsApp)

  pass
