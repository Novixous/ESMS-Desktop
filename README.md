# ESMS-Desktop
***packaging**
Use this command:
pyinstaller --add-data="Detection/haarcascade_frontalface_default.xml;Detection" --add-binary="Detection\Weight\model-epoch-30.h5;Detection\Weight" --onefile main.py