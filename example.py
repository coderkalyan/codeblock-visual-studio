import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QStatusBar, QLabel, QTableView, \
    QWidget, QHeaderView, QGridLayout, QFrame, QComboBox, QHBoxLayout, QDockWidget, QFileDialog, QMenu

# noinspection PyUnresolvedReferences

class MainWindow(QMainWindow):
    shortcuts = {
        "QUIT": "Ctrl+W",
        "ADD": "Ctrl+N",
        "EDIT": "Ctrl+I",
        "OPEN": "Ctrl+O",
        "OPEN-LEGACY": "Ctrl+Shift+O",
        "CREATE": "Ctrl+Shift+N",
        "SETTINGS": "Ctrl+Alt+S",
        "MANAGE-SCHEDULES": ""
    }

    icons = {
        "QUIT": ":/small/quit",
        "ADD": ":/medium/add",
        "EDIT": ":/medium/edit",
        "OPEN": ":/small/open",
        "OPEN-LEGACY": ":/small/open",
        "CREATE": ":/small/create",
        "SETTINGS": ":/small/settings",
        "MANAGE-SCHEDULES": ":/small/manage",
        "REMOVE": ":/medium/remove",
        "WINDOW": ":/small/window"
    }

    def __init__(self):
        super().__init__(flags=Qt.Window)

        # setup actions
        self.status_bar = self.statusBar()
        self.tool_bar = self.addToolBar("Video")
        # TODO: icon sizes
        self.tool_bar.setIconSize(QSize(36, 36))
        # add the following 3 lines back in if you want the buttons to be right aligned
        # spacer = QWidget()
        # spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.tool_bar.addWidget(spacer)
        self.action_quit = QAction("Quit")
        self.action_quit.setShortcut(self.shortcuts["QUIT"])
        self.action_quit.setIcon(QIcon(QPixmap(self.icons["QUIT"])))
        self.action_quit.triggered.connect(self.close)

        self.action_add = QAction("Add Video")
        self.action_add.setShortcut(self.shortcuts["ADD"])
        self.action_add.setIcon(QIcon(QPixmap(self.icons["ADD"])))
        self.action_add.triggered.connect(self.add_video)

        self.action_edit = QAction("Edit Video Options")
        self.action_edit.setShortcut(self.shortcuts["EDIT"])
        self.action_edit.setIcon(QIcon(QPixmap(self.icons["EDIT"])))
        self.action_edit.triggered.connect(lambda: print("Action Edit Video"))

        self.action_open = QAction("Open")
        self.action_open.setShortcut(self.shortcuts["OPEN"])
        self.action_open.setIcon(QIcon(QPixmap(self.icons["OPEN"])))
        self.action_open.triggered.connect(lambda: print("Action Open"))

        self.action_open_legacy = QAction("Open Legacy File(.vst)")
        self.action_open_legacy.setShortcut(self.shortcuts["OPEN-LEGACY"])
        self.action_open_legacy.setIcon(QIcon(QPixmap(self.icons["OPEN-LEGACY"])))
        self.action_open_legacy.triggered.connect(lambda: print("Action Open Legacy"))

        self.action_create = QAction("Create Schedule")
        self.action_create.setShortcut(self.shortcuts["CREATE"])
        self.action_create.setIcon(QIcon(QPixmap(self.icons["CREATE"])))
        self.action_create.triggered.connect(self.create_schedule)

        self.action_settings = QAction("Settings")
        self.action_settings.setShortcut(self.shortcuts["SETTINGS"])
        self.action_settings.setIcon(QIcon(QPixmap(self.icons["SETTINGS"])))
        self.action_settings.triggered.connect(lambda: print("Action Settings"))

        self.action_remove = QAction("Remove Video")
        # self.action_remove.setShortcut(self.shortcuts["REMOVE"])
        self.action_remove.setIcon(QIcon(QPixmap(self.icons["REMOVE"])))
        self.action_remove.triggered.connect(self.table_right_clicked)
        # build views
        self.central_widget = QWidget(self, Qt.Widget)
        self.main_layout = QGridLayout()
        self.central_widget.setLayout(self.main_layout)

        self.schedule_layout = QHBoxLayout()
        picker_text = QLabel()
        picker_text.setText("Select Schedule:")
        self.schedule_picker = QComboBox()
        self.schedule_picker.currentIndexChanged.connect(lambda x: print("Picker!"))
        self.schedule_picker.addItems(["Item 1", "Item 2", "Item 3"])
        self.schedule_layout.addWidget(self.schedule_picker)
        self.main_layout.addWidget(picker_text, 0, 0)
        self.main_layout.addChildLayout(self.schedule_layout)
        self.main_layout.addWidget(self.schedule_picker, 0, 1)
        self.video_table_view = QTableView(self)
        self.video_table_view.hideColumn(0)
        self.video_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.video_table_view, 1, 0, 1, 4)
        self.video_table_view.customContextMenuRequested.connect(lambda: "right click")

        self.inspect_video_window = QDockWidget()
        lbl = QLabel()
        lbl.setText("I am a dock window label!")
        self.inspect_video_window.setWidget(lbl)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.inspect_video_window)
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def add_video(self):
        # when add video event is clicked
        # does nothing - child will override this method
        pass

    def create_schedule(self):
        # when create schedule event is clicked
        # does nothing - child will override this method
        pass

    def table_right_clicked(self, position):
        print("Right clicked")
        menu = QMenu()
        menu.addAction(self.action_remove)
        menu.exec_(self.ui.table_videos.viewport().mapToGlobal(position))
        pass

    @staticmethod
    def default_event():
        # this is what all the onClicks, menu buttons, etc. get connected to by default
        # it does nothing - is just a placeholder
        pass

    def init_ui(self):
        self.setWindowTitle("Video Scheduler")
        self.setWindowIcon(QIcon(QPixmap(self.icons["WINDOW"])))

        #with open("../darkstyle.qss") as f:
        #    self.setStyleSheet(f.read())
        self.resize(800, 600)
        self.setup_menu_bar()
        self.setup_toolbar()
        self.post_status_message()

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self.action_create)
        file_menu.addAction(self.action_open)
        file_menu.addAction(self.action_open_legacy)

        file_menu.addSeparator()
        file_menu.addAction(self.action_settings)
        file_menu.addSeparator()
        file_menu.addAction(self.action_quit)

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(self.action_add)
        edit_menu.addAction(self.action_edit)

    def setup_toolbar(self):
        self.tool_bar.show()
        self.tool_bar.addAction(self.action_add)
        self.tool_bar.addAction(self.action_edit)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def post_status_message(self):
        # status_bar_layout = self.status_bar.layout()
        now_playing = QLabel()
        now_playing.setText("Now playing: video1.mp4")
        time_left = QLabel()
        time_left.setText("Time left: 5:05")
        line = QFrame(self, Qt.Widget)
        # line.setObjectName(QString.fromUtf8("line"))
        # line.setGeometry(QRect(320, 150, 118, 3))
        # line.setSiz
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        # status_bar_layout.addWidget(now_playing)
        self.status_bar.addWidget(now_playing)
        self.status_bar.addWidget(line)
        self.status_bar.addWidget(time_left)

    @staticmethod
    def table_double_clicked(index):
        print(index.column())
        if index.column() == 0:
            # we want to open a file dialog to choose new video
            filename, status = QFileDialog.getOpenFileName(caption="Choose Video File")
            print(filename)
        else:
            return

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
