import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import alembic
import types


def abc_tree(i_obj):
    tree_dict = {}
    for index in xrange(i_obj.getNumChildren()):
        child = i_obj.getChild(index)
        tree_dict[child.getName()] = abc_tree(child)
    return tree_dict


def get_abc_tree(i_path):
    i_archive = alembic.Abc.IArchive(str(i_path))
    i_archive.getTop().getName()
    tree_dict = abc_tree(i_archive.getTop())
    return tree_dict


class ListAlembic(QDialog):

    def __init__(self, parent=None):
        super(ListAlembic, self).__init__(parent)
        # Create widgets
        self.resize(300, 500)
        self.alembic_file = '/home/shrimo/Desktop/course/vfx_dev/alembic/abc_list.abc'
        self.setWindowTitle("Alembic tree")
        self.l1 = QLabel(self.alembic_file.split('/')[-1])
        self.button = QPushButton("Load alembic")

        self.abc_tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.abc_tree_view.setModel(self.model)
        self.set_tree_view()

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.abc_tree_view)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.button.clicked.connect(self.load_abc)

    def set_tree_view(self):
        # set Tree View
        self.abc_tree_view.reset()
        self.model.clear()
        self.root = QStandardItem('ABC')
        self.make_tree(get_abc_tree(self.alembic_file), self.root)
        self.model.appendRow(self.root)
        self.abc_tree_view.expandAll()

    def make_tree(self, children, parent):
        for child in children:
            child_item = QStandardItem(child)
            parent.appendRow(child_item)
            if isinstance(children, types.DictType):
                self.make_tree(children[child], child_item)

    def load_abc(self):
        self.alembic_file = QFileDialog.getOpenFileName(
            self, 'Open *. abc file', '/home/shrimo/Desktop/course/vfx_dev/alembic')[0]
        self.l1.setText(self.alembic_file.split('/')[-1]) 
        self.set_tree_view()


if __name__ == '__main__':
    # alembic_file = '/home/shrimo/Desktop/course/vfx_dev/alembic/abc_list.abc'
    # print get_abc_tree(alembic_file)
    app = QApplication(sys.argv)
    # Create and show the ListAlembic
    list_alembic = ListAlembic()
    list_alembic.show()
    sys.exit(app.exec_())
