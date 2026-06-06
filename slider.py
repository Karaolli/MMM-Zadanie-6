from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox, QSlider
from PySide6.QtCore import Qt, Signal

class Slider(QWidget):
    valueChanged = Signal(float)
    def __init__(self, name, desc, parent=None):
        super().__init__(parent)
        self.step_size = desc["step"]
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(name)
        self.label.setFixedWidth(71)
        layout.addWidget(self.label)

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(desc["min"], desc["max"])
        self.spinbox.setValue(desc["default"])
        self.spinbox.setSingleStep(desc["step"])
        self.spinbox.setFixedWidth(55)
        self.spinbox.valueChanged.connect(self._on_spinbox)
        layout.addWidget(self.spinbox)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(desc["min"] / self.step_size, desc["max"] / self.step_size)
        self.slider.setValue(desc["default"] / self.step_size)
        self.slider.valueChanged.connect(self._on_slider)
        layout.addWidget(self.slider)

    def _on_spinbox(self, value):
        self.slider.blockSignals(True)
        self.slider.setValue(value / self.step_size)
        self.slider.blockSignals(False)
        self.valueChanged.emit(value)

    def _on_slider(self, value):
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(value * self.step_size)
        self.spinbox.blockSignals(False)
        self.valueChanged.emit(value * self.step_size)