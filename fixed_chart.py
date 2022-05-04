from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.factory import Factory as F
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from icecream import ic
from kivy.metrics import dp,sp
from graphs import AKBarChart


Builder.load_string("""
<Barchart>
    size_hint_y: None
    height: dp(200)
    label_size: sp(12)
    bg_color: 202/255,202/255,202/255,1
    bars_color: 128/255,0,0,1
    labels_color: 0,0,0,1
    anim: True
    on_y_values: self.update()

<ScreenOne>:
    rv: rv.__self__
    RecycleView:
        id: rv
        viewclass: 'Barchart'
        data: root.data
        RecycleBoxLayout:
            size_hint: (1, None)
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(20)
            orientation: 'vertical'
            default_size_hint: 1, None
            default_size: None, dp(200)
""")

class Barchart(AKBarChart, RecycleDataViewBehavior):
    x_values = F.ListProperty([1, 2, 3, 4, 5])
    y_values = F.ListProperty([1, 2, 3, 4, 5])

    def refresh_view_attrs(self, rv, index, data):
        self.x_values = data['x_values']
        self.y_values = data['y_values']
        return super().refresh_view_attrs(rv, index, data)

data = [
    {   
        'x_values': [i, i + 1, i + 2, i + 3],
        'y_values': [10*i, 20*i, 30*i, 40*i],
    } for i in range(9)
] 

class ScreenOne(F.Screen):
    data = data

class MyApp(MDApp):
    def build(self):
        return ScreenOne()

MyApp().run()
