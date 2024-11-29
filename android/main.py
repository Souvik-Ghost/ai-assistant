from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Title
        title = Label(
            text='Ghost Smart Assistant',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # Features
        features = BoxLayout(orientation='vertical', size_hint_y=0.9)
        
        # Add feature buttons
        buttons = [
            'Visual Detection',
            'Audio Detection',
            'Device Monitoring',
            'Internet Search',
            'OSINT Tools'
        ]
        
        for button_text in buttons:
            btn = Button(
                text=button_text,
                size_hint_y=0.2,
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=self.switch_screen)
            features.add_widget(btn)
        
        layout.add_widget(features)
        self.add_widget(layout)
    
    def switch_screen(self, instance):
        screen_name = instance.text.lower().replace(' ', '_')
        self.manager.current = screen_name

class GhostAssistantApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    GhostAssistantApp().run()