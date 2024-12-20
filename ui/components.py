from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTreeWidget, QComboBox, QSpinBox, QTextEdit, QFileDialog, QTreeWidgetItem, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import os

class PathSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Input Location")
        browse_input_btn = QPushButton("Browse")
        browse_input_btn.clicked.connect(self.browse_input)

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Save Location")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(self.browse_output)

        layout.addWidget(QLabel("Input Location:"))
        layout.addWidget(self.input_path)
        layout.addWidget(browse_input_btn)
        layout.addWidget(QLabel("Save Location:"))
        layout.addWidget(self.output_path)
        layout.addWidget(browse_output_btn)
        self.setLayout(layout)

    def browse_input(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_path.setText(folder)

    def browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path.setText(folder)

class FileTreeView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.input_tree = QTreeWidget()
        self.input_tree.setHeaderLabel("Input Files")
        self.output_tree = QTreeWidget()
        self.output_tree.setHeaderLabel("Output Structure")

        layout.addWidget(self.input_tree)
        layout.addWidget(self.output_tree)
        self.setLayout(layout)
    def load_directory(self, path):
        self.input_tree.clear()
        if not os.path.exists(path):
            return

        def add_items(parent, folder_path):
            try:
                # Создаем словарь для хранения пар файлов
                media_files = {"video": {}, "audio": {}}

                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    tree_item = QTreeWidgetItem(parent, [item])

                    if os.path.isdir(item_path):
                        # Папки
                        tree_item.setForeground(0, QColor("yellow"))
                        add_items(tree_item, item_path)

                        # Проверяем, есть ли внутри медиафайлы
                        if any(os.path.isfile(os.path.join(item_path, f)) for f in os.listdir(item_path)):
                            tree_item.setForeground(0, QColor("blue"))
                    else:
                        # Файлы
                        ext = os.path.splitext(item)[-1].lower()
                        base_name = os.path.splitext(item)[0]  # Имя файла без расширения

                        if ext in [".mp4", ".mkv", ".mov"]:
                            tree_item.setForeground(0, QColor("red"))  # Отметим как одиночный файл
                            media_files["video"][base_name] = tree_item

                        elif ext in [".mp3", ".wav"]:
                            tree_item.setForeground(0, QColor("red"))  # Отметим как одиночный файл
                            media_files["audio"][base_name] = tree_item

                        else:
                            tree_item.setForeground(0, QColor("purple"))  # Немедиафайлы

                # Сопоставляем пары и обновляем цвет узлов
                for base_name, video_item in media_files["video"].items():
                    if base_name in media_files["audio"]:
                        video_item.setForeground(0, QColor("green"))  # Видео готово к склейке
                        audio_item = media_files["audio"][base_name]
                        audio_item.setForeground(0, QColor("green"))  # Аудио готово к склейке

            except PermissionError:
                pass

        root_item = QTreeWidgetItem(self.input_tree, [os.path.basename(path)])
        add_items(root_item, path)
        root_item.setExpanded(True)


class OptionsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP4", "MKV", "MOV"])

        self.video_codec_combo = QComboBox()
        self.video_codec_combo.addItems(["h264"])

        self.audio_codec_combo = QComboBox()
        self.audio_codec_combo.addItems(["aac"])

        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setRange(1, 16)
        self.threads_spinbox.setValue(4)

        layout.addWidget(QLabel("Format:"))
        layout.addWidget(self.format_combo)
        layout.addWidget(QLabel("Video Codec:"))
        layout.addWidget(self.video_codec_combo)
        layout.addWidget(QLabel("Audio Codec:"))
        layout.addWidget(self.audio_codec_combo)
        layout.addWidget(QLabel("Threads:"))
        layout.addWidget(self.threads_spinbox)

        self.setLayout(layout)

class StartButtonWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("font-size: 18px; height: 50px;")
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

class LogConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setPlaceholderText("Log output will appear here...")
        layout.addWidget(self.log_console)

        self.setLayout(layout)