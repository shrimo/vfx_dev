import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import alembic

# def list_nodes(i_obj, abc_nodes = []):
#     abc_nodes.append(str(i_obj))
#     for index in xrange(i_obj.getNumChildren()):
#         i_child = i_obj.getChild(index)
#         list_nodes(i_child, abc_nodes)
#     return abc_nodes

def list_nodes(i_obj, abc_nodes = []):
    abc_nodes.append(str(i_obj))
    for index in xrange(i_obj.getNumChildren()):
        i_child = i_obj.getChild(index)
        list_nodes(i_child, abc_nodes)
    return abc_nodes

def list_abc(i_path):
    i_archive = alembic.Abc.IArchive(i_path)
    i_archive.getTop().getName()
    return list_nodes(i_archive.getTop())

class ListAlembic(QDialog):

    def __init__(self, parent=None):
        super(ListAlembic, self).__init__(parent)
        # Create widgets
        self.resize(300, 500)
        self.alembic_file = '/home/shrimo/Desktop/course/vfx_dev/alembic/abc_separation_in.abc'
        self.setWindowTitle("Alembic list")
        self.l1 = QLabel("Alembic object tree")
        self.button = QPushButton("Reload")

        # create Tree View
        self.abc_list = QTreeView()
        self.model = QStandardItemModel()
        self.addItems(self.model, list_abc(self.alembic_file))
        self.abc_list.setModel(self.model)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.abc_list)
        layout.addWidget(self.button)
        # self.load_tree()
        
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.load_abc)

    def load_tree(self):
        abc_tree = list_abc(self.alembic_file)
        parent = QStandardItem('root')
        for branch in abc_tree:
            # print branch
            parent.appendRow(QStandardItem(branch))
        self.model.appendRow(parent)

    def addItems(self, parent, elements):
        for child in elements:
            item = QStandardItem(child)
            parent.appendRow(item)
    
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