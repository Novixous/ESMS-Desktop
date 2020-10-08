import kivy
kivy.require('1.9.0')
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '340')
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from screens.login_screen import LoginScreen
from screens.session_screen import SessionScreen
from kivymd.app import MDApp

class LoginScreenWrapper(Screen):
  pass

class SessionScreenWrapper(Screen):
  pass

class ESMSApp(MDApp):
  screen_manager = ScreenManager(transition=NoTransition())
  login_screen_wrp = None
  session_screen_wrp = None

  def __init__(self, **kwargs):
    super(ESMSApp, self).__init__(**kwargs)

  def build(self):
    self.theme_cls.primary_palette = 'BlueGray'

    self.login_screen_wrp = LoginScreenWrapper(name='login')
    self.session_screen_wrp = SessionScreenWrapper(name='session')

    self.screen_manager.add_widget(self.login_screen_wrp)
    self.screen_manager.add_widget(self.session_screen_wrp)

    return self.screen_manager

def main():
  ESMSApp().run()


if __name__ == '__main__':
  main()
