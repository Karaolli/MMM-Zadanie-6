import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel, QPushButton
from PySide6.QtCore import Qt
import simulation
import signals
from slider import Slider

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

class MainWindow(QMainWindow):
    parameter_descriptions_signal = {
        "Częstotl. [Hz]": {"min":0   , "max":100, "default":1  , "step":0.01},
        "Faza [°]"      : {"min":0   , "max":360, "default":0  , "step":0.01},
        "Długość [s]"   : {"min":0.01, "max":100, "default":1  , "step":0.01},
        "Długość [%]"   : {"min":0   , "max":100, "default":100, "step":0.01},
        "Krok [ms]"     : {"min":0.01, "max":100, "default":1  , "step":0.01}}

    parameter_descriptions_system = {
        "R [Ω]"         : {"min":0   , "max":100, "default":1  , "step":0.01},
        "L [H]"         : {"min":0.01, "max":100, "default":1  , "step":0.01},
        "K_T"           : {"min":0   , "max":100, "default":1  , "step":0.01},
        "K_e"           : {"min":0   , "max":100, "default":1  , "step":0.01},
        "J"             : {"min":0.01, "max":100, "default":1  , "step":0.01},
        "k"             : {"min":0   , "max":100, "default":1  , "step":0.01}}

    parameter_descriptions_x0 = {
        "i(0)"          : {"min":-10 , "max":10 , "default":0  , "step":0.01},
        "θ'(0)"         : {"min":-10 , "max":10 , "default":0  , "step":0.01},
        "θ(0)"          : {"min":-10 , "max":10 , "default":0  , "step":0.01}}
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MMM Zadanie 6 206620 203578")

        central_widget = QSplitter(Qt.Orientation.Horizontal)
        central_widget.setChildrenCollapsible(False)
        central_widget.setHandleWidth(8)
        central_widget.setStyleSheet("QSplitter::handle { background-color: #aaaaaa; }")
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout(central_widget)


        plot_widget = QWidget()
        plot_widget.setMinimumWidth(400)
        central_layout.addWidget(plot_widget)
        plot_layout = QVBoxLayout(plot_widget)

        self.plot_figure, self.plot_axes = plt.subplots()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        plot_layout.addWidget(self.plot_canvas)

        plot_buttons_layout = QHBoxLayout()
        plot_layout.addLayout(plot_buttons_layout)

        self.btn_current = QPushButton("Prąd")
        self.btn_current.clicked.connect(lambda: self._toggle_plot(0))
        plot_buttons_layout.addWidget(self.btn_current)

        self.btn_speed = QPushButton("Prędkość")
        self.btn_speed.clicked.connect(lambda: self._toggle_plot(1))
        plot_buttons_layout.addWidget(self.btn_speed)

        self.btn_position = QPushButton("Położenie")
        self.btn_position.clicked.connect(lambda: self._toggle_plot(2))
        plot_buttons_layout.addWidget(self.btn_position)


        controls_widget = QWidget()
        controls_widget.setMinimumWidth(400)
        central_layout.addWidget(controls_widget)
        controls_layout = QVBoxLayout(controls_widget)


        signal_label = QLabel("Parametry sygnału:")
        controls_layout.addWidget(signal_label, alignment=Qt.AlignCenter)

        signal_layout = QHBoxLayout()
        controls_layout.addLayout(signal_layout)

        self.btn_sine = QPushButton("Sinus")
        self.btn_sine.clicked.connect(self._on_sine)
        signal_layout.addWidget(self.btn_sine)

        self.btn_square = QPushButton("Prostokąt")
        self.btn_square.clicked.connect(self._on_square)
        signal_layout.addWidget(self.btn_square)

        self.btn_sawtooth = QPushButton("Trójkąt")
        self.btn_sawtooth.clicked.connect(self._on_triangle)
        signal_layout.addWidget(self.btn_sawtooth)


        self.params = {}

        self.parameter_sliders = {}

        for name, desc in self.parameter_descriptions_signal.items():
            self.params[name] = self.parameter_descriptions_signal[name]["default"]
            self.parameter_sliders[name] = Slider(name, desc)
            self.parameter_sliders[name].valueChanged.connect(lambda value, name=name: self._on_change(name, value))
            controls_layout.addWidget(self.parameter_sliders[name])

        system_label = QLabel("Parametry układu:")
        controls_layout.addWidget(system_label, alignment=Qt.AlignCenter)

        for name, desc in self.parameter_descriptions_system.items():
            self.params[name] = self.parameter_descriptions_system[name]["default"]
            self.parameter_sliders[name] = Slider(name, desc)
            self.parameter_sliders[name].valueChanged.connect(lambda value, name=name: self._on_change(name, value))
            controls_layout.addWidget(self.parameter_sliders[name])

        x0_label = QLabel("Warunki początkowe:")
        controls_layout.addWidget(x0_label, alignment=Qt.AlignCenter)

        for name, desc in self.parameter_descriptions_x0.items():
            self.params[name] = self.parameter_descriptions_x0[name]["default"]
            self.parameter_sliders[name] = Slider(name, desc)
            self.parameter_sliders[name].valueChanged.connect(lambda value, name=name: self._on_change(name, value))
            controls_layout.addWidget(self.parameter_sliders[name])


        central_widget.setSizes([1, 1])

        self.chosen_plots = [True, True, True]

        self._on_sine()

    def _update_signal(self):
        if self.signal_type == "sine":
            self.signal = signals.sine    (self.params["Częstotl. [Hz]"], self.params["Faza [°]"], self.params["Długość [s]"], self.params["Długość [%]"] * 0.01, self.params["Krok [ms]"] * 0.001)
        if self.signal_type == "square":
            self.signal = signals.square  (self.params["Częstotl. [Hz]"], self.params["Faza [°]"], self.params["Długość [s]"], self.params["Długość [%]"] * 0.01, self.params["Krok [ms]"] * 0.001)
        if self.signal_type == "sawtooth":
            self.signal = signals.sawtooth(self.params["Częstotl. [Hz]"], self.params["Faza [°]"], self.params["Długość [s]"], self.params["Długość [%]"] * 0.01, self.params["Krok [ms]"] * 0.001)
        A, B, C, D = simulation.make_state_model(self.params["R [Ω]"], self.params["L [H]"], self.params["K_T"], self.params["K_e"], self.params["J"], self.params["k"])
        self.y = simulation.simulate([[self.params["i(0)"]], [self.params["θ'(0)"]], [self.params["θ(0)"]]], self.signal[1], self.params["Krok [ms]"] * 0.001, A, B, C, D)
        self._plot()

    def _plot(self):
        self.plot_axes.clear()
        for i, enabled in enumerate(self.chosen_plots):
            if enabled:
                self.plot_axes.plot(self.signal[0], self.y[:, i], color=colors[i])
        self.plot_axes.plot(self.signal[0], self.signal[1], color=colors[4])
        self.plot_axes.set_xlabel("Time (s)")
        self.plot_canvas.draw()

    def _toggle_plot(self, index : int):
        self.chosen_plots[index] = not self.chosen_plots[index]
        self._plot()

    def _on_sine(self):
        self.signal_type = "sine"
        self.btn_sine    .setEnabled(False)
        self.btn_square  .setEnabled(True)
        self.btn_sawtooth.setEnabled(True)
        self._update_signal()

    def _on_square(self):
        self.signal_type = "square"
        self.btn_sine    .setEnabled(True)
        self.btn_square  .setEnabled(False)
        self.btn_sawtooth.setEnabled(True)
        self._update_signal()

    def _on_triangle(self):
        self.signal_type = "sawtooth"
        self.btn_sine    .setEnabled(True)
        self.btn_square  .setEnabled(True)
        self.btn_sawtooth.setEnabled(False)
        self._update_signal()
    
    def _on_change(self, name, value):
        self.params[name] = value
        self._update_signal()
