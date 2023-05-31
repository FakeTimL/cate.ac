from django.apps import AppConfig

initialized = False

class MainConfig(AppConfig):
  name = 'main'
  
  def ready(self):
    global initialized
    if not initialized:
      print('Initializing app `main`...')
      initialized = True
      import main.signals # Connect signal receivers
