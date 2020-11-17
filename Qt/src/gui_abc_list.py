import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import alembic
import types


def abc_tree(i_obj):
    '''
    create dict by alembic tree
    '''
    tree_dict = {}
    for index in xrange(i_obj.getNumChildren()):
        child = i_obj.getChild(index)
        tree_dict[child.getName()] = abc_tree(child)
    return tree_dict


def get_abc_tree(i_path):
    '''
    Load alembic file and get top level objet
    '''
    i_archive = alembic.Abc.IArchive(str(i_path))
    i_archive.getTop().getName()
    return abc_tree(i_archive.getTop())


class ListAlembic(QWidget):
    '''
    Create GUI for alembic file tree view
    '''

    def __init__(self, parent=None):
        super(ListAlembic, self).__init__(parent)
        # Create widgets
        print ('Alembic tree viewer 0.0.1')
        self.resize(300, 500)
        self.setStyleSheet("color: #dedede; background-color: #212121")
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        self.alembic_file = '/home/shrimo/Desktop/course/vfx_dev/alembic/abc_list.abc'
        self.setWindowTitle("Alembic tree")
        self.l1 = QLabel(self.alembic_file.split('/')[-1])
        self.button = QPushButton("Load alembic")

        self.abc_tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.abc_tree_view.setModel(self.model)
        self.set_tree_view()
        # self.load_abc()

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.abc_tree_view)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.button.clicked.connect(self.load_abc)
        self.sys_tray()

    def sys_tray(self):
        icon = QIcon("alembic_logo.png")
        menu = QMenu()
        menu.setStyleSheet("color: #dedede; background-color: #212121")
        settingAction = menu.addAction("Load alembic")
        settingAction.triggered.connect(self.load_abc)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(sys.exit)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip("Alembic tree view")
        self.tray.showMessage("note", "load alembic file")

    def set_tree_view(self):
        '''
        Set Tree View
        '''
        self.abc_tree_view.reset()
        self.model.clear()
        self.root = QStandardItem('ABC')
        self.make_tree(get_abc_tree(self.alembic_file), self.root)
        self.model.appendRow(self.root)
        self.abc_tree_view.expandAll()

    def make_tree(self, children, parent):
        '''
        Make tree view by dict
        '''
        for child in children:
            child_item = QStandardItem(child)
            parent.appendRow(child_item)
            if isinstance(children, types.DictType):
                self.make_tree(children[child], child_item)

    def load_abc(self):
        '''
        GUI for load alembic file
        '''
        self.alembic_file = QFileDialog.getOpenFileName(
            self, 'Open *. abc file', '/home/shrimo/Desktop/course/vfx_dev/alembic', filter='*.abc')[0]
        if not self.alembic_file:
            self.l1.setText('No file')
            return
        self.l1.setText(self.alembic_file.split('/')[-1])
        self.set_tree_view()

    def __del__(self): 
        print ('Exit application')


if __name__ == '__main__':
    # Create and show the ListAlembic
    app = QApplication(sys.argv)
    list_alembic = ListAlembic()
    list_alembic.show()
    sys.exit(app.exec_())
