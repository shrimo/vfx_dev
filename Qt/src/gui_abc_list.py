import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import alembic
import types


def abc_tree(i_obj, tree_list={}):
    for index in xrange(i_obj.getNumChildren()):
        child = i_obj.getChild(index)
        tree_list[i_obj.getName()] = child.getName()
        abc_tree(child, tree_list)
    return tree_list


def get_abc_tree(i_path):
    i_archive = alembic.Abc.IArchive(i_path)
    i_archive.getTop().getName()
    tree_dict = abc_tree(i_archive.getTop())
    del tree_dict['ABC']
    return tree_dict


class ListAlembic(QDialog):

    def __init__(self, parent=None):
        super(ListAlembic, self).__init__(parent)
        # Create widgets
        self.resize(300, 500)
        self.alembic_file = '/home/shrimo/Desktop/course/vfx_dev/alembic/abc_separation_in.abc'
        self.setWindowTitle("Alembic list")
        self.l1 = QLabel("Alembic object tree")
        self.button = QPushButton("Reload")

        # get_abc_tree(self.alembic_file)

        # create Tree View
        self.abc_list = QTreeView()
        self.model = QStandardItemModel()
        # self.load_tree()
        self.abc_list.setModel(self.model)
        self._populateTree(get_abc_tree(self.alembic_file), self.model)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.abc_list)
        layout.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.load_abc)

    def _populateTree(self, children, parent):
        for child in sorted(children):
            child_item = QStandardItem(child)
            parent.appendRow(child_item)
            if isinstance(children, types.DictType):
                self._populateTree(children[child], child_item)

    # def load_tree(self):
    #     abc_tree = get_abc_tree(self.alembic_file)
    #     parent = QStandardItem('root')
    #     for branch in abc_tree:
    #         item = QStandardItem(branch)
    #         item.appendRow(QStandardItem(item))
    #     parent.appendRow(item)
    #     self.model.appendRow(parent)

    # Open alembic file

    def load_abc(self):
        # for i in range(3):
        fname = QFileDialog.getOpenFileName(self, 'Open *. abc file', '/home')
        print fname


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the ListAlembic
    list_alembic = ListAlembic()
    list_alembic.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
