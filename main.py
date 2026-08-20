import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from gtts import gTTS

API_KEY = "AIzaSyC88C4nnLNUianzAVIY8r6z7C_5n6uhUUY"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"

class FridayUI(BoxLayout):
    def __init__(self, **kwargs):
        super(FridayUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(
            text="[b]FRIDAY AI ASSISTANT[/b]", 
            markup=True, 
            font_size='22sp', 
            size_hint_y=0.1
        ))

        self.chat_history = Label(
            text="Friday: Hello Boss, Friday App System is Online.", 
            size_hint_y=None, 
            font_size='16sp',
            halign='left',
            valign='top'
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.75))
        scroll.add_widget(self.chat_history)
        self.add_widget(scroll)

        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        self.user_input = TextInput(hint_text="Type your command...", multiline=False)
        send_btn = Button(text="Send", size_hint_x=0.3, on_press=self.process_input)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        self.add_widget(input_layout)

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang='bn')
            tts.save("voice.mp3")
            os.system("mpv voice.mp3 > /dev/null 2>&1")
            if os.path.exists("voice.mp3"):
                os.remove("voice.mp3")
        except:
            pass

    def process_input(self, instance):
        text = self.user_input.text.strip()
        if text:
            self.chat_history.text += f"\n\nYou: {text}"
            self.user_input.text = ""
            reply = self.ask_gemini(text)
            self.chat_history.text += f"\nFriday: {reply}"
            self.speak(reply)

    def ask_gemini(self, prompt):
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": f"You are Friday, Tony Stark's AI assistant. Answer concisely.\nUser: {prompt}"}]}]}
        try:
            response = requests.post(URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            return "System error occurred."
        except:
            return "Network connection error."

class FridayApp(App):
    def build(self):
        return FridayUI()

if __name__ == '__main__':
    FridayApp().run()
