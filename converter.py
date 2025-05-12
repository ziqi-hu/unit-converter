import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, 
                            QGridLayout, QScrollArea, QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon


class UnitConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("科学单位转换工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置中文字体
        font = QFont("SimHei", 10)
        self.setFont(font)
        
        # 创建主部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # 创建历史记录区域
        self.history_area = QScrollArea()
        self.history_area.setWidgetResizable(True)
        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_area.setWidget(self.history_widget)
        self.history_area.setMaximumHeight(150)
        self.main_layout.addWidget(self.history_area)
        
        # 初始化各单位转换标签页
        self.create_energy_tab()
        self.create_length_tab()
        self.create_time_tab()
        
        # 初始化历史记录
        self.history_items = []
        self.update_history()
        
    def create_energy_tab(self):
        """创建能量转换标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.StyledPanel)
        input_layout = QHBoxLayout(input_frame)
        
        input_value_layout = QVBoxLayout()
        input_value_layout.addWidget(QLabel("输入值:"))
        self.energy_input_value = QLineEdit()
        self.energy_input_value.setPlaceholderText("输入数值")
        input_value_layout.addWidget(self.energy_input_value)
        input_layout.addLayout(input_value_layout)
        
        input_unit_layout = QVBoxLayout()
        input_unit_layout.addWidget(QLabel("输入单位:"))
        self.energy_input_unit = QComboBox()
        self.energy_input_unit.addItems([
            "au (原子单位)", "cm⁻¹ (波数)", "eV (电子伏)", 
            "J (焦耳)", "kJ/mol (千焦每摩尔)", "kcal/mol (千卡每摩尔)",
            "MHz (兆赫兹)", "K (开尔文)", "nm (纳米，波长)"
        ])
        input_unit_layout.addWidget(self.energy_input_unit)
        input_layout.addLayout(input_unit_layout)
        
        layout.addWidget(input_frame)
        
        # 结果区域
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel)
        result_layout = QGridLayout(result_frame)
        
        self.energy_result_labels = {}
        units = [
            "au (原子单位)", "cm⁻¹ (波数)", "eV (电子伏)", 
            "J (焦耳)", "kJ/mol (千焦每摩尔)", "kcal/mol (千卡每摩尔)",
            "MHz (兆赫兹)", "K (开尔文)", "nm (纳米，波长)"
        ]
        
        for i, unit in enumerate(units):
            row = i // 3
            col = i % 3
            
            unit_label = QLabel(unit)
            result_label = QLabel("--")
            result_label.setAlignment(Qt.AlignRight)
            result_label.setStyleSheet("font-weight: bold; color: #165DFF;")
            
            self.energy_result_labels[unit] = result_label
            
            result_layout.addWidget(unit_label, row, col*2)
            result_layout.addWidget(result_label, row, col*2+1)
        
        layout.addWidget(result_frame)
        
        # 转换按钮
        convert_button = QPushButton("转换")
        convert_button.setStyleSheet("background-color: #FF7D00; color: white; font-weight: bold; padding: 8px;")
        convert_button.clicked.connect(lambda: self.convert_units("energy"))
        layout.addWidget(convert_button, alignment=Qt.AlignCenter)
        
        self.tabs.addTab(tab, "能量转换")
    
    def create_length_tab(self):
        """创建长度转换标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.StyledPanel)
        input_layout = QHBoxLayout(input_frame)
        
        input_value_layout = QVBoxLayout()
        input_value_layout.addWidget(QLabel("输入值:"))
        self.length_input_value = QLineEdit()
        self.length_input_value.setPlaceholderText("输入数值")
        input_value_layout.addWidget(self.length_input_value)
        input_layout.addLayout(input_value_layout)
        
        input_unit_layout = QVBoxLayout()
        input_unit_layout.addWidget(QLabel("输入单位:"))
        self.length_input_unit = QComboBox()
        self.length_input_unit.addItems([
            "au (原子单位)", "Å (埃)", "nm (纳米)", "cm (厘米)", "m (米)"
        ])
        input_unit_layout.addWidget(self.length_input_unit)
        input_layout.addLayout(input_unit_layout)
        
        layout.addWidget(input_frame)
        
        # 结果区域
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel)
        result_layout = QGridLayout(result_frame)
        
        self.length_result_labels = {}
        units = [
            "au (原子单位)", "Å (埃)", "nm (纳米)", "cm (厘米)", "m (米)"
        ]
        
        for i, unit in enumerate(units):
            row = i // 3
            col = i % 3
            
            unit_label = QLabel(unit)
            result_label = QLabel("--")
            result_label.setAlignment(Qt.AlignRight)
            result_label.setStyleSheet("font-weight: bold; color: #165DFF;")
            
            self.length_result_labels[unit] = result_label
            
            result_layout.addWidget(unit_label, row, col*2)
            result_layout.addWidget(result_label, row, col*2+1)
        
        layout.addWidget(result_frame)
        
        # 转换按钮
        convert_button = QPushButton("转换")
        convert_button.setStyleSheet("background-color: #FF7D00; color: white; font-weight: bold; padding: 8px;")
        convert_button.clicked.connect(lambda: self.convert_units("length"))
        layout.addWidget(convert_button, alignment=Qt.AlignCenter)
        
        self.tabs.addTab(tab, "长度转换")
    
    def create_time_tab(self):
        """创建时间转换标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.StyledPanel)
        input_layout = QHBoxLayout(input_frame)
        
        input_value_layout = QVBoxLayout()
        input_value_layout.addWidget(QLabel("输入值:"))
        self.time_input_value = QLineEdit()
        self.time_input_value.setPlaceholderText("输入数值")
        input_value_layout.addWidget(self.time_input_value)
        input_layout.addLayout(input_value_layout)
        
        input_unit_layout = QVBoxLayout()
        input_unit_layout.addWidget(QLabel("输入单位:"))
        self.time_input_unit = QComboBox()
        self.time_input_unit.addItems([
            "fs (飞秒)", "ps (皮秒)", "ns (纳秒)", "µs (微秒)", "s (秒)", "h (小时)"
        ])
        input_unit_layout.addWidget(self.time_input_unit)
        input_layout.addLayout(input_unit_layout)
        
        layout.addWidget(input_frame)
        
        # 结果区域
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel)
        result_layout = QGridLayout(result_frame)
        
        self.time_result_labels = {}
        units = [
            "fs (飞秒)", "ps (皮秒)", "ns (纳秒)", "µs (微秒)", "s (秒)", "h (小时)"
        ]
        
        for i, unit in enumerate(units):
            row = i // 3
            col = i % 3
            
            unit_label = QLabel(unit)
            result_label = QLabel("--")
            result_label.setAlignment(Qt.AlignRight)
            result_label.setStyleSheet("font-weight: bold; color: #165DFF;")
            
            self.time_result_labels[unit] = result_label
            
            result_layout.addWidget(unit_label, row, col*2)
            result_layout.addWidget(result_label, row, col*2+1)
        
        layout.addWidget(result_frame)
        
        # 转换按钮
        convert_button = QPushButton("转换")
        convert_button.setStyleSheet("background-color: #FF7D00; color: white; font-weight: bold; padding: 8px;")
        convert_button.clicked.connect(lambda: self.convert_units("time"))
        layout.addWidget(convert_button, alignment=Qt.AlignCenter)
        
        self.tabs.addTab(tab, "时间转换")
    
    def convert_units(self, category):
        """执行单位转换"""
        try:
            # 获取输入值
            if category == "energy":
                value = float(self.energy_input_value.text())
                input_unit = self.energy_input_unit.currentText().split(" ")[0]
                result_labels = self.energy_result_labels
                factors = self.get_energy_factors()
            elif category == "length":
                value = float(self.length_input_value.text())
                input_unit = self.length_input_unit.currentText().split(" ")[0]
                result_labels = self.length_result_labels
                factors = self.get_length_factors()
            elif category == "time":
                value = float(self.time_input_value.text())
                input_unit = self.time_input_unit.currentText().split(" ")[0]
                result_labels = self.time_result_labels
                factors = self.get_time_factors()
            
            # 转换单位并更新结果
            for unit_text, label in result_labels.items():
                unit = unit_text.split(" ")[0]
                if unit == input_unit:
                    continue
                
                factor = factors[input_unit][unit]
                result = value * factor
                
                # 格式化结果
                if abs(result) >= 1e4 or abs(result) < 1e-3:
                    formatted_result = f"{result:.6e}"
                else:
                    formatted_result = f"{result:.6f}".rstrip('0').rstrip('.')
                
                label.setText(formatted_result)
            
            # 添加到历史记录
            self.add_to_history(category, value, input_unit)
            
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的数值！")
    
    def get_energy_factors(self):
        """获取能量单位转换因子"""
        return {
            'au': {
                'au': 1.0,
                'cm⁻¹': 219474.63,
                'eV': 27.211386,
                'J': 4.359744e-18,
                'kJ/mol': 2625.50,
                'kcal/mol': 627.509,
                'MHz': 6.579684e9,
                'K': 3.157746e5,
                'nm': 45.56335
            },
            'cm⁻¹': {
                'au': 1/219474.63,
                'cm⁻¹': 1.0,
                'eV': 0.000123984,
                'J': 1.986445e-23,
                'kJ/mol': 0.0119626,
                'kcal/mol': 0.00285914,
                'MHz': 29979.2458,
                'K': 1.438777,
                'nm': 1e7
            },
            'eV': {
                'au': 1/27.211386,
                'cm⁻¹': 8065.544,
                'eV': 1.0,
                'J': 1.602177e-19,
                'kJ/mol': 96.4853,
                'kcal/mol': 23.0605,
                'MHz': 2.417989e8,
                'K': 1.160452e4,
                'nm': 1239.842
            },
            'J': {
                'au': 1/4.359744e-18,
                'cm⁻¹': 5.03411e22,
                'eV': 6.241509e18,
                'J': 1.0,
                'kJ/mol': 6.022141e23,
                'kcal/mol': 1.439323e23,
                'MHz': 1.509190e26,
                'K': 7.24297e22,
                'nm': 1.986445e26
            },
            'kJ/mol': {
                'au': 1/2625.50,
                'cm⁻¹': 83.59347,
                'eV': 0.01036427,
                'J': 1.660539e-21,
                'kJ/mol': 1.0,
                'kcal/mol': 0.239006,
                'MHz': 2.506075e7,
                'K': 1.202724e3,
                'nm': 1.196266e8
            },
            'kcal/mol': {
                'au': 1/627.509,
                'cm⁻¹': 349.755,
                'eV': 0.0433641,
                'J': 6.94770e-21,
                'kJ/mol': 4.184,
                'kcal/mol': 1.0,
                'MHz': 1.04694e8,
                'K': 5.03217e3,
                'nm': 4.96565e7
            },
            'MHz': {
                'au': 1/6.579684e9,
                'cm⁻¹': 3.335641e-5,
                'eV': 4.135667e-9,
                'J': 6.626070e-34,
                'kJ/mol': 3.990313e-8,
                'kcal/mol': 9.537175e-9,
                'MHz': 1.0,
                'K': 4.799244e-5,
                'nm': 2.997924e14
            },
            'K': {
                'au': 1/3.157746e5,
                'cm⁻¹': 0.6950347,
                'eV': 8.617333e-5,
                'J': 1.380649e-23,
                'kJ/mol': 0.000831447,
                'kcal/mol': 1.987205e-4,
                'MHz': 2.083661e4,
                'K': 1.0,
                'nm': 1.438777e7
            },
            'nm': {
                'au': 1/45.56335,
                'cm⁻¹': 1e7,
                'eV': 1239.842,
                'J': 1.986445e-25,
                'kJ/mol': 1.196266e-7,
                'kcal/mol': 2.859144e-8,
                'MHz': 2.997924e14,
                'K': 1.438777e7,
                'nm': 1.0
            }
        }
    
    def get_length_factors(self):
        """获取长度单位转换因子"""
        return {
            'au': {
                'au': 1.0,
                'Å': 0.5291772,
                'nm': 0.05291772,
                'cm': 5.291772e-9,
                'm': 5.291772e-11
            },
            'Å': {
                'au': 1/0.5291772,
                'Å': 1.0,
                'nm': 0.1,
                'cm': 1e-8,
                'm': 1e-10
            },
            'nm': {
                'au': 1/0.05291772,
                'Å': 10.0,
                'nm': 1.0,
                'cm': 1e-7,
                'm': 1e-9
            },
            'cm': {
                'au': 1/5.291772e-9,
                'Å': 1e8,
                'nm': 1e7,
                'cm': 1.0,
                'm': 0.01
            },
            'm': {
                'au': 1/5.291772e-11,
                'Å': 1e10,
                'nm': 1e9,
                'cm': 100.0,
                'm': 1.0
            }
        }
    
    def get_time_factors(self):
        """获取时间单位转换因子"""
        return {
            'fs': {
                'fs': 1.0,
                'ps': 0.001,
                'ns': 1e-6,
                'µs': 1e-9,
                's': 1e-15,
                'h': 2.777778e-19
            },
            'ps': {
                'fs': 1000.0,
                'ps': 1.0,
                'ns': 0.001,
                'µs': 1e-6,
                's': 1e-12,
                'h': 2.777778e-16
            },
            'ns': {
                'fs': 1e6,
                'ps': 1000.0,
                'ns': 1.0,
                'µs': 0.001,
                's': 1e-9,
                'h': 2.777778e-13
            },
            'µs': {
                'fs': 1e9,
                'ps': 1e6,
                'ns': 1000.0,
                'µs': 1.0,
                's': 1e-6,
                'h': 2.777778e-10
            },
            's': {
                'fs': 1e15,
                'ps': 1e12,
                'ns': 1e9,
                'µs': 1e6,
                's': 1.0,
                'h': 0.0002777778
            },
            'h': {
                'fs': 3.6e18,
                'ps': 3.6e15,
                'ns': 3.6e12,
                'µs': 3.6e9,
                's': 3600.0,
                'h': 1.0
            }
        }
    
    def add_to_history(self, category, value, unit):
        """添加转换记录到历史"""
        # 格式化类别名称
        category_names = {
            'energy': '能量',
            'length': '长度',
            'time': '时间'
        }
        category_name = category_names.get(category, category)
        
        # 添加到历史列表
        import datetime
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_items.append(f"{now} - {category_name}转换: {value} {unit}")
        
        # 限制历史记录数量
        if len(self.history_items) > 10:
            self.history_items = self.history_items[-10:]
        
        # 更新历史显示
        self.update_history()
    
    def update_history(self):
        """更新历史记录显示"""
        # 清空现有历史记录
        for i in reversed(range(self.history_layout.count())):
            self.history_layout.itemAt(i).widget().setParent(None)
        
        # 添加"暂无转换历史"提示
        if not self.history_items:
            label = QLabel("暂无转换历史")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #86909C; font-style: italic;")
            self.history_layout.addWidget(label)
            return
        
        # 添加历史记录项
        for item in self.history_items:
            label = QLabel(item)
            label.setStyleSheet("border-bottom: 1px solid #E5E6EB; padding: 4px 0;")
            self.history_layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = UnitConverter()
    converter.show()
    sys.exit(app.exec_())    
