import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QSlider, QLabel)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MySignalSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("信号处理交互系统 (PyQt5)")
        self.resize(800, 600)

        # 1. 核心组件初始化
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QHBoxLayout(self.main_widget) # 左右布局

        # 左侧控制面板
        self.control_panel = QVBoxLayout()
        self.label = QLabel("余弦波频率: 2 Hz")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 10)
        self.slider.setValue(2)
        self.slider.valueChanged.connect(self.update_label)

        self.btn_generate = QPushButton("生成信号波形")
        self.btn_clear = QPushButton("清除数据")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.control_panel.addWidget(self.label)
        self.control_panel.addWidget(self.slider)
        self.control_panel.addWidget(self.btn_generate)
        self.control_panel.addWidget(self.btn_clear)
        self.control_panel.addWidget(QLabel("实验状态信息:"))
        self.control_panel.addWidget(self.text_edit)

        # 右侧绘图区域
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        self.layout.addLayout(self.control_panel, 1)
        self.layout.addWidget(self.canvas, 3)

        # 2. 信号与槽绑定 (这是我之前给你的核心逻辑)
        self.btn_generate.clicked.connect(self.update_plot)
        self.btn_clear.clicked.connect(self.clear_data)

    def update_label(self, value):
        self.label.setText(f"余弦波频率: {value} Hz")

    def update_plot(self):
        """更新绘图区域并记录状态"""
        freq = self.slider.value()
        t = np.linspace(0, 1, 1000)
        y = np.cos(2 * np.pi * freq * t)
        
        self.ax.clear()
        self.ax.plot(t, y, color='dodgerblue')
        self.ax.set_title(f"连续信号: cos(2 * pi * {freq} * t)")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw() 
        
        # 对应你报告中的日志输出
        self.text_edit.append(f"[状态] 更新波形成功（频率 {freq}Hz）")

    def clear_data(self):
        self.ax.clear()
        self.canvas.draw()
        self.text_edit.append("[状态] 数据已清除")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySignalSystem()
    window.show()
    sys.exit(app.exec_())
