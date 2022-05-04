from helper import point_on_circle
from draw_tools import DrawTools
from kivy.uix.relativelayout import RelativeLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp

from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)

Builder.load_string("""
<AKChartLabel>
    theme_text_color: "Custom"
    text_color: root._owner.labels_color if root._owner else [1, 1, 1, 1]
    halign: "center"
    valign: "center"
    adaptive_width: True
    size_hint_y: None
<AKChartBase>
    padding: dp(30)
    _labels_y_box: _labels_y_box
    _labels_x_box: _labels_x_box
    _canvas: _canvas
    target_canvas: _canvas.canvas.after
    # Layout to draw main shapes
    BoxLayout:
        id: _canvas
        canvas.before:
            Color:
                rgba: root.bg_color if root.bg_color else root.theme_cls.primary_color
            RoundedRectangle:
                pos: self.pos
                size: root.size
                radius: root.radius if root.radius else [dp(5), ]
        
    # Y axis labels
    RelativeLayout:
        id: _labels_y_box
    # X axis labels
    RelativeLayout:
        id: _labels_x_box

""")

class AKChartLabel(MDLabel):
    _owner = ObjectProperty()
    _mypos = ListProperty([0, 0])

class AKChartBase(DrawTools, ThemableBehavior, RelativeLayout):
    x_values = ListProperty([])
    x_labels = ListProperty([])
    y_values = ListProperty([])
    y_labels = ListProperty([])
    bg_color = ColorProperty(None, allownone=True)
    radius = ListProperty(None, alllownone=True)
    anim = BooleanProperty(True)
    d = NumericProperty(1)
    t = StringProperty("out_quad")
    labels = BooleanProperty(True)
    labels_color = ColorProperty([1, 1, 1, 1])
    label_size = NumericProperty("15dp")
    bars_color = ColorProperty([1, 1, 1, 1])
    line_width = NumericProperty("2dp")
    lines_color = ColorProperty([1, 1, 1, 1])
    lines = BooleanProperty(True)
    trim = BooleanProperty(True)
    _loaded = NumericProperty(1)
    _labels_y_box = ObjectProperty()
    _labels_x_box = ObjectProperty()
    _canvas = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self._myinit = True
        self.bind(
            _loaded=lambda *args: self._update(anim=True),
        )
        Clock.schedule_once(self.update)

    def _get_normalized_cor(self, val, mode, f_update=1):
        x_values = self.x_values
        y_values = self.y_values
        trim = self.trim
        padding = self.padding
        size = self.size
        min_x = min(x_values) if trim else 0
        max_x = max(x_values)
        min_y = min(y_values) if trim else 0
        max_y = max(y_values)
        x_distance = (max_x - min_x) if trim else max_x
        y_distance = (max_y - min_y) if trim else max_y

        if mode == "x":
            _min = min_x
            _distance = x_distance
            _size = size[0]
            f_update = 1
        else:
            _min = min_y
            _distance = y_distance
            _size = size[1]

        try:
            res = ((val - _min) / _distance) * (
                _size - self._bottom_line_y() - padding
            )

            final_y = f_update * val/max_y*130
        except:
            final_y = 6
        return final_y


    def do_layout(self, *args, **kwargs):
        super().do_layout(*args, **kwargs)
        self._update()

    def update(self, *args):
        self._myinit = True
        if self.anim:
            print('starting animation')
            self._loaded = 0
            anim = Animation(_loaded=1, t=self.t, d=self.d)
            anim.start(self)
        else:
            self._update()
            self._update()

    def _update(self, anim=False, *args):
        x_values = self.x_values
        y_values = self.y_values
        x_labels = self.x_labels
        y_labels = self.y_labels
        canvas = self._canvas.canvas
        canvas.clear()
        canvas.after.clear()
        if self._myinit:
            self._labels_y_box.clear_widgets()
            self._labels_x_box.clear_widgets()

        dis = self._bottom_line_y()
        self.draw_shape(
            "line",
            shape_name="line",
            canvas=canvas,
            points=[
                [dis, dis],
                [self.width - dis, dis],
            ],
            line_width=self.line_width,
            color=self.lines_color,
        )

        if not x_values or not y_values:
            raise Exception("x_values and y_values cannot be empty")

        if len(x_values) != len(y_values):
            raise Exception("x_values and y_values must have equal length")

        if (
            ((len(x_labels) != len(y_values)) and len(x_labels) > 0)
            or (len(y_labels) != len(y_values))
            and len(y_labels) > 0
        ):
            raise Exception(
                "x_values and y_values and x_labels must have equal length"
            )

    def _bottom_line_y(self):
        return self.label_size * 2

    def draw_label(self, text_x, text_y, center_pos_x, center_pos_y, idx):
        labels_y_box = self._labels_y_box
        labels_x_box = self._labels_x_box
        if self._myinit:
            label_y = AKChartLabel(
                text=str(int(float(text_y))) if text_y.isnumeric() else text_y,
                center=center_pos_y,
                _owner=self,
                height=self.label_size * 2,
            )
            label_y.font_size = self.label_size
            label_x = AKChartLabel(
                text=text_x,
                center=center_pos_x,
                _owner=self,
                height=self.label_size * 2,
            )
            label_x.font_size = self.label_size
            labels_y_box.add_widget(label_y)
            labels_x_box.add_widget(label_x)
        else:
            child_y = labels_y_box.children[idx]
            child_x = labels_x_box.children[idx]
            child_y.center_x = center_pos_y[0]
            child_y.y = center_pos_y[1]
            child_x.center_x = center_pos_x[0]
            child_x.y = center_pos_x[1]



class AKBarChart(AKChartBase):
    max_bar_width = NumericProperty("80dp")
    min_bar_width = NumericProperty("10dp")
    bars_spacing = NumericProperty("10dp")
    bars_radius = NumericProperty("5dp")
    bars_color = ColorProperty([1, 1, 1, 1])

    def _update(self, anim=False, *args):
        super()._update()
        x_values = self.x_values
        y_values = self.y_values
        canvas = self._canvas.canvas
        drawer = self.draw_shape
        # bottom line
        bottom_line_y = self._bottom_line_y()
        count = len(self.y_values)
        bars_x_list = self.get_bar_x(count)
        bar_width = self.get_bar_width()
        f_update = self._loaded if anim else 1
        for i in range(0, count):
            x = x_values[i]
            x_label = self.x_labels[i] if self.x_labels else False
            y_label = self.y_labels[i] if self.y_labels else False
            y = y_values[i]
            new_x = bars_x_list[i]
            new_y = self._get_normalized_cor(y, "y", f_update)

            drawer(
                "bars",
                shape_name="roundedRectangle",
                canvas=canvas.after,
                color=self.bars_color,
                radius=[self.bars_radius, self.bars_radius, 0, 0],
                size=[bar_width, new_y],
                pos=[new_x, bottom_line_y],
            )

            if self.labels:
                y_pos = [new_x + bar_width / 2, new_y + dp(24)]
                x_pos = [new_x + bar_width / 2, 0]
                self.draw_label(
                    text_x=x_label if x_label else str(x),
                    text_y=y_label if y_label else str(y),
                    center_pos_x=x_pos,
                    center_pos_y=y_pos,
                    idx=len(x_values) - i - 1,
                )
        self._myinit = False


    def get_bar_x(self, bar_count):
        bar_width = self.get_bar_width()
        total_width = (
            bar_width * bar_count
            + (bar_count - 1) * self.bars_spacing
            + self.label_size * 4
        )
        start_pos = (self.width - total_width) / 2
        x_list = []
        for x in range(0, bar_count):
            x_pos = (
                start_pos
                + (bar_width + self.bars_spacing) * x
                + self.label_size * 2
            )
            x_list.append(x_pos)
        return x_list

    def get_bar_width(self):
        bars_count = len(self.x_values)
        spacing = self.bars_spacing
        width = self.width
        bar_width = (
            width - (bars_count + 1) * spacing - self.label_size * 4
        ) / bars_count
        if bar_width > self.max_bar_width:
            return self.max_bar_width
        elif bar_width < self.min_bar_width:
            return self.min_bar_width
        else:
            return bar_width