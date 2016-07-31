from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        fontName='fonts/NanumGothic.ttf'
        return Button(text="Heelo World\n안녕?", font_name=fontName)
TestApp().run()
