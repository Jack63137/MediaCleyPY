from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .components import PathSelectionWidget, FileTreeView, OptionsWidget, StartButtonWidget, LogConsoleWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Converter")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Add components
        self.path_selection = PathSelectionWidget()
        main_layout.addWidget(self.path_selection)

        self.file_tree_view = FileTreeView()
        main_layout.addWidget(self.file_tree_view)

        self.options_widget = OptionsWidget()
        main_layout.addWidget(self.options_widget)

        self.start_button = StartButtonWidget()
        main_layout.addWidget(self.start_button)

        self.log_console = LogConsoleWidget()
        main_layout.addWidget(self.log_console)

        # Connect signals
        self.path_selection.input_path.textChanged.connect(self.update_file_tree)
        
    def update_file_tree(self):
        input_path = self.path_selection.input_path.text()
        print(f"Updating file tree with path: {input_path}")  # Для отладки
        self.file_tree_view.load_directory(input_path)
