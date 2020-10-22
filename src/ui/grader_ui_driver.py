from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from ui.make_ui import Ui_MainWindow
from grades import Grades
from file_ops import copy_student_by_sid
from utils import *


class GraderUiDriver(Ui_MainWindow):
    def __init__(self, grades):
        """
        :type grades: grades.Grades
        """
        vprint("Creating UI")
        super(GraderUiDriver, self).__init__()
        self.state = grades

    def make_mark_widgets(self):
        """
        customizes the grading window to hold entries for each mark requirement
        """
        delete_layout_subelements(self.grades_layout)  # removes dummy widgets
        self.mark_lines = {}
        for requirement, value in self.state.template.items():
            grade_layout = QHBoxLayout()
            grade_layout.setObjectName("grade_layout")
            req_label = QLabel(self.centralwidget)
            req_label.setObjectName("req_label")
            req_label.setText(requirement)
            grade_layout.addWidget(req_label)
            grade_edit = QLineEdit(self.centralwidget)
            grade_edit.setMaximumSize(QSize(30, 16777215))
            grade_edit.setObjectName(requirement)
            self.mark_lines[requirement] = grade_edit
            grade_layout.addWidget(grade_edit)
            total_label = QLabel(self.centralwidget)
            total_label.setMaximumSize(QSize(30, 16777215))
            total_label.setObjectName("total_label")
            total_label.setText("/" + str(value))
            grade_layout.addWidget(total_label)
            self.grades_layout.addLayout(grade_layout)

    def bind_buttons(self):
        self.btn_load.clicked.connect(self.load)
        self.btn_prev.clicked.connect(self.prev)
        self.btn_next.clicked.connect(self.next)
        self.btn_save.clicked.connect(self.save)
        self.btn_complete.clicked.connect(self.complete)

    def save(self):
        data = self.state.curr_data()
        # get data from text fields
        # grades
        for requirement, mark_line in self.mark_lines.items():
            grade = mark_line.text()
            if grade.isdigit():
                data["grade"][requirement]["mark"] = int(mark_line.text())
        # partners
        data["partners"] = self.partner_line.text()
        # comments
        data["comments"] = self.comment_text.toPlainText()
        self.state.save()
        self.redraw()

    def load(self):
        self.state.copy_current()

    def next(self):
        self.state.next()
        self.redraw()

    def prev(self):
        self.state.prev()
        self.redraw()

    def complete(self):
        m = self.state.curr_data().get("marked")
        self.state.curr_data()["marked"] = not m
        self.redraw()

    def redraw(self):
        data = self.state.curr_data()
        # nameplate
        sid = self.state.cur_id()
        full_name = self.state.curr_name()
        curr = self.state.curr
        total = self.state.total
        marked = "(Incomplete)"
        if data.get("marked"):
            marked = "(Complete)"
        nameplate_str = f"{sid}-{full_name} {marked}\t({curr}/{total})"
        self.nameplate.setText(nameplate_str)
        # comment
        self.comment_text.setPlainText(data.get("comments"))
        partners = data.get("partners")
        self.partner_line.setText(partners)
        # grades
        for requirement, grade_val in self.state.template.items():
            mark_line = self.mark_lines[requirement]
            s_grade = data['grade'][requirement]["mark"]
            if s_grade is None:
                mark_line.setText("")
            else:
                mark_line.setText(str(s_grade))
        # progress bar
        self.progressBar.setValue(self.state.progress())


def bind_window_and_run(grader_ui):
    """
    :type grader_ui: GraderUiDriver
    """
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    grader_ui.setupUi(MainWindow)
    grader_ui.bind_buttons()
    grader_ui.make_mark_widgets()
    grader_ui.redraw()
    MainWindow.show()
    sys.exit(app.exec_())


def delete_layout_subelements(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                delete_layout_subelements(item.layout())
