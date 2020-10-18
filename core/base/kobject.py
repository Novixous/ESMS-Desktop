from kivy.app import App

class KObject:
  def __init__(self, skip_self_register=False, **kwargs):
    cls = f'{self.__class__.__name__}'.lower()
    self.kid = cls
    esmsApp = App.get_running_app()

    setattr(self, 'app', esmsApp)

    if not skip_self_register:
      setattr(esmsApp, cls, self)

  pass
