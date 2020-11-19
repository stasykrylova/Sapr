import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from nodalsDia import Ui_Dialog_Nodal_Loads
from sterloads import Ui_Dialog_Rod_Loads
from sterDi import Ui_Dialog_Stergen_Dialog
from StoppingDialog import Ui_Dialog_Stopping_Dialog
from MPLForWidget import MyMPlCanvas
from realMain import Ui_MainWindow
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from MyGraphics import MyGraphics
from Stergen import Rod
from widget import Ui_Dialog_Draw_Widget
from epur import Epur_Ui_Dialog
from graf import Graf_Ui_Dialog
from table import Table_Ui_Dialog

from chooseRod import Choose_Ui_Dialog
from chooseStep import Choose_Step_Ui_Dialog

import math

from PyQt5.QtWidgets import QErrorMessage
import json
from Counting import Counting
datasForGraf=[]
myGraf =MyGraphics()
znach=0
StoppIsDone=0
RodIsDone=0
stop_code=0
nodal_loads={}
rod_loads={}
json_dict = {}
count_code=0


class Get_step_reply(QDialog,Choose_Step_Ui_Dialog):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow
        self.pushButton.clicked.connect(self.acpt_data)
        self.lineEdit.setReadOnly(True)

    def acpt_data(self):
            step=self.lineEdit_2.text()
            if is_digit(step):
                self.mainwindow.step_rod=float(step)

                self.close()
            else:
                self.lineEdit_2.setStyleSheet("background-color: rgb(218, 112, 214)")


class TableDialogWindow(QDialog, Table_Ui_Dialog):
    def __init__(self, mainwindow,data):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow = mainwindow
        # Кол-во рядов меняется в зависимости от значений в data.
        print("table is inited")
        self.tableWidget.setRowCount(
            len(data)
        )
        # Кол-во столбцов меняется в зависимости от data.
        self.tableWidget.setColumnCount(
            len(data[0])-1
        )

        self.tableWidget.setHorizontalHeaderLabels(
            ('X', 'N(x)','U(x)','S(x)')
        )
        print("Table is done")

        row = 0
        for tup in data:
            col = 0

            for item in tup[:4]:
                cellinfo = QTableWidgetItem(item)
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                )
                print(cellinfo)
                self.tableWidget.setItem(row, col, cellinfo)
                print("Done")
                col += 1


            row += 1
        row_=0
        for tup in data:
            if math.fabs(float(tup[3]))>math.fabs(float(tup[4])):
                self.tableWidget.item(row_, 3).setBackground(QColor(171, 79, 86))
            row_+=1





class Get_i_reply(QDialog,Choose_Ui_Dialog):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow
        self.pushButton.clicked.connect(self.acpt_data)
        self.lineEdit.setReadOnly(True)
        str_box_second = []
        if count_code != 0:
            for i in range(1, len(datasForGraf) + 1):
                str_box_second.append(str(i))
            self.comboBox.addItems(str_box_second)

            self.comboBox.activated[str].connect(self.onActivated)
            self.i = "1"
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала рассчитайте конструкцию!')
            error_dialog.exec_()

    def acpt_data(self):
        if stop_code!=0:
            self.mainwindow.i_rod=int(self.i)-1
            print(self.mainwindow.i_rod)
        self.close()


    def onActivated(self, text):
        self.i = text


class GrafDialogWindow(QDialog, Graf_Ui_Dialog):
    def __init__(self, mainwindow, fig):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow

        self.fig_N, self.fig_U , self.fig_S= fig
        print("Okay")

        self.companovka_for_mpl_N= QVBoxLayout(self.widget_3)
        self.companovka_for_mpl_U = QVBoxLayout(self.widget_4)
        self.companovka_for_mpl_S = QVBoxLayout(self.widget_5)

        self.canavas_N=MyMPlCanvas(self.fig_N)
        self.canavas_U = MyMPlCanvas(self.fig_U)
        self.canavas_S= MyMPlCanvas(self.fig_S)

        self.companovka_for_mpl_N.addWidget(self.canavas_N)
        self.companovka_for_mpl_U.addWidget(self.canavas_U)
        self.companovka_for_mpl_S.addWidget(self.canavas_S)


class EpurDialogWindow(QDialog, Epur_Ui_Dialog):
    def __init__(self, mainwindow, fig):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow

        self.pushButton.clicked.connect(self.getDatas)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)

        self.fig_U, self.fig_N = fig

        self.companovka_for_mpl_N= QVBoxLayout(self.widget_2)
        self.companovka_for_mpl_U = QVBoxLayout(self.widget_3)

        self.canavas_N=MyMPlCanvas(self.fig_N)
        self.canavas_U = MyMPlCanvas(self.fig_U)

        self.companovka_for_mpl_N.addWidget(self.canavas_N)
        self.companovka_for_mpl_U.addWidget(self.canavas_U)

        #self.toolbar= NavigationToolbar(self.canavas,self)
        #self.companovka_for_mpl.addWidget(self.toolbar)
        #self.label.setPixmap(QPixmap('construction.png'))
        #self.label.setGeometry(0, 0, 1500, 1500)

    def getDatas(self):
        print("Clicked")
        self.lineEdit_2.setStyleSheet("background-color: white")
        x_line = self.lineEdit_2.text()
        if is_digit(x_line):
            x=float(x_line)
            N,U,S=self.mainwindow.newCount.getDatas(x)
            self.lineEdit_3.setText('{:.5f}'.format(N))
            self.lineEdit_4.setText('{:.5f}'.format(U))
            self.lineEdit_5.setText('{:.5f}'.format(S))
        else:
            self.lineEdit_2.setStyleSheet("background-color: red")


class DrawDialogWindow(QDialog, Ui_Dialog_Draw_Widget):
    def __init__(self, mainwindow,fig):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow
        self.pushButton.clicked.connect(self.deth)

        self.companovka_for_mpl= QVBoxLayout(self.widget)
        self.canavas=MyMPlCanvas(fig)
        self.companovka_for_mpl.addWidget(self.canavas)
        self.toolbar= NavigationToolbar(self.canavas,self)
        self.companovka_for_mpl.addWidget(self.toolbar)
        #self.label.setPixmap(QPixmap('construction.png'))
        #self.label.setGeometry(0, 0, 1500, 1500)

    def deth(self):
        self.widget.close()
        self.widget.update()
        self.show()
        self.close()






class StergenDialogWindow(QDialog, Ui_Dialog_Stergen_Dialog):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow

        self.pushButton.clicked.connect(self.acpting_datas)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_answer.setReadOnly(True)


        self.znach=0



    def acpting_datas(self):
        self.lineEdit_2.setStyleSheet("background-color: white")
        self.lineEdit_3.setStyleSheet("background-color: white")
        self.lineEdit_4.setStyleSheet("background-color: white")
        self.lineEdit_5.setStyleSheet("background-color: white")

        length_line= self.lineEdit_2.text()
        pl_line= self.lineEdit_5.text()
        modUpr_line=self.lineEdit_3.text()
        dopuskNapr_line=self.lineEdit_4.text()

        if is_digit(length_line):
            
                if is_digit(pl_line):

                        if  is_digit(modUpr_line):


                                if is_digit(dopuskNapr_line):



                                        global RodIsDone
                                        RodIsDone=1

                                        pl = float(pl_line)
                                        length = int(length_line)
                                        modUpr = float(modUpr_line)
                                        dopuskNapr = float(dopuskNapr_line)
                                        if len(datasForGraf) == 0:
                                            i = 1
                                            pred_end_coord = [1, 2]
                                            pred_len = 0
                                            pred_height = 0
                                            pred_height_for_draw = 0

                                        else:

                                            rodneeded = datasForGraf[-1]
                                            i = len(datasForGraf) + 1

                                            pred_end_coord = rodneeded.end_coordinates
                                            pred_len = rodneeded.length
                                            pred_height = rodneeded.area
                                            pred_height_for_draw = rodneeded.height_for_draw

                                        new_rod = Rod(length, pl, modUpr, dopuskNapr, i, pred_end_coord, pred_len, pred_height,
                                                      pred_height_for_draw)

                                        datasForGraf.append(new_rod)
                                        myGraf.rod_init(new_rod.start_coordinates, new_rod.height_for_draw, new_rod.length_for_draw,
                                                        length, self.znach)
                                        self.znach += 1
                                        fig = myGraf.drawEverything()
                                        self.mainwindow.showConstruct(fig)
                                        self.close()

                                else:
                                    self.lineEdit_4.setStyleSheet("background-color: rgb(218, 112, 214)")
                                    self.lineEdit_answer.setText("Значение должно быть числовым")

                        else:
                            self.lineEdit_3.setStyleSheet("background-color: rgb(218, 112, 214)")
                            self.lineEdit_answer.setText("Значение должно быть числовым")

                else:
                    self.lineEdit_5.setStyleSheet("background-color: rgb(218, 112, 214)")
                    self.lineEdit_answer.setText("Значение должно быть числовым")

        else:
            self.lineEdit_2.setStyleSheet("background-color: rgb(218, 112, 214)")
            self.lineEdit_answer.setText("Значение должно быть числовым")



    def rjcting_data(self):
        self.close()


class StoppDialogWindow(QDialog,Ui_Dialog_Stopping_Dialog):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow
        self.buttonBox.accepted.connect(self.acpt_data)
        self.buttonBox.rejected.connect(self.rjct_data)
        self.comboBox.addItem("Правая заделка")
        self.comboBox.addItem("Левая заделка")
        self.comboBox.addItem("Обе заделки")
        self.comboBox.activated[str].connect(self.onActivated)
        self.stop="Правая заделка"

    def acpt_data(self):
        global stop_code
        if RodIsDone==1:
            if self.stop=="Правая заделка":
                stop_code=2
                datasForGraf[-1].setStop()
            if self.stop=="Левая заделка":
                stop_code=1
                datasForGraf[0].setStop()
            if self.stop=="Обе заделки":
                stop_code=3
                datasForGraf[-1].setStop()
                datasForGraf[0].setStop()

            fig = myGraf.drawEverything(stop_code)
            self.mainwindow.showConstruct(fig)
            self.close()
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала введите стержни!')
            error_dialog.exec_()
    def rjct_data(self):
        self.close()
    def onActivated(self,text):
        self.stop=text


class NodalLoadsDialogWindow(QDialog,Ui_Dialog_Nodal_Loads):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow= mainwindow
        self.pushButton.clicked.connect(self.acpt_data)
        self.lineEdit.setReadOnly(True)

        str_box=[]
        if stop_code !=0:
          for i in range (1,len(datasForGraf)+2):
            str_box.append(str(i))
          self.comboBox.addItems(str_box)

          self.comboBox.activated[str].connect(self.onActivated)
          self.nodal_load = "1"
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала введите заделки!')
            error_dialog.exec_()


    def acpt_data(self):
        global nodal_loads
        load_value_line= self.lineEdit_2.text()



        if stop_code!= 0:
            if is_digit(load_value_line) and not is_float(load_value_line):
                load_value = int(load_value_line)
                nodal_loads[int(self.nodal_load)] = load_value
                #myGraf.nodal_loads_init(nodal_loads[-1],load_value)

                fig = myGraf.drawEverything(stop_code,load_value, int(self.nodal_load))
                self.mainwindow.showConstruct(fig)
                self.close()
            else:
                self.lineEdit_2.setStyleSheet("background-color: rgb(218, 112, 214)")
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала введите заделки!')
            error_dialog.exec_()

    def rjct_data(self):
        self.close()

    def onActivated(self, text):
        self.nodal_load = text


class RodLoadsDialogWindow(QDialog, Ui_Dialog_Rod_Loads):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.pushButton.clicked.connect(self.acpt_data)
        self.lineEdit.setReadOnly(True)

        str_box_second = []
        if stop_code != 0:
            for i in range(1, len(datasForGraf) + 1):
                str_box_second.append(str(i))
            self.comboBox.addItems(str_box_second)

            self.comboBox.activated[str].connect(self.onActivated)
            self.rod_load = "1"
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала введите заделки!')
            error_dialog.exec_()


    def acpt_data(self):
        global rod_loads
        rod_value_line = self.lineEdit_2.text()

        if stop_code != 0:
            if is_digit(rod_value_line) and not is_float(rod_value_line):
                rod_value = int(rod_value_line)
                rod_loads[int(self.rod_load)] = rod_value
                # myGraf.nodal_loads_init(nodal_loads[-1],load_value)

                fig = myGraf.drawEverything(stop_code,0,0, rod_value, int(self.rod_load))
                self.mainwindow.showConstruct(fig)
                self.close()
            else:
                self.lineEdit_2.setStyleSheet("background-color: rgb(218, 112, 214)")
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала введите заделки!')
            error_dialog.exec_()

    def rjct_data(self):
        self.close()

    def onActivated(self, text):
        self.rod_load = text



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.pushButton.clicked.connect(self.Save)
        self.pushButton_2.clicked.connect(self.GoCount)

        self.pushButton_5.setText("Добавить стержень")
        self.pushButton_5.clicked.connect(self.newSter)
        self.pushButton_6.setText("Добавить заделки")
        self.pushButton_6.clicked.connect(self.newStop)
        self.pushButton_7.setText("Узловые нагрузки")
        self.pushButton_7.clicked.connect(self.newNoalLoad)
        self.pushButton_4.setText("Стержневые нагрузки")
        self.pushButton_4.clicked.connect(self.newRodLoad)
        self.pushButton_8.clicked.connect(self.DrawDia)
        self.pushButton_9.clicked.connect(self.DrawGr)
        self.pushButton_10.clicked.connect(self.ShowTable)

        self.newCount = Counting()



    def Save(self):
        #Словарь: 1:{}, заделки:{} , нагрузки на стержень:{}, нагрузки на узел:{}
        if stop_code != 0:
            dict_rods={}
            for i in range(len(datasForGraf)):
               dict_rods[i + 1] = datasForGraf[i].getDatas()
            json_dict["Rods"]=dict_rods
            if stop_code == 1:
                json_dict["Stopps"] = "Left"
            elif stop_code == 2:
                json_dict["Stopps"] = "Right"
            else:
                json_dict["Stopps"] = "Both"
            json_dict["Rod loads"]=rod_loads
            json_dict["Nodal loads"]= nodal_loads

            with open("construct.json", "w") as write_file:
                json.dump(json_dict, write_file)
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала введите заделки!')
            error_dialog.exec_()



    def get_step(self):
        self.step_rod = 0
        DialogSecondIns = Get_step_reply(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()

    def get_i_rod(self):
        self.i_rod = 0
        DialogSecondIns = Get_i_reply(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()


    def DrawDia(self):
        if count_code != 0:
            fig_Dia = self.newCount.makeDiagram()
            self.showDiagram(fig_Dia)
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала рассчитайте конструкцию!')
            error_dialog.exec_()


    def DrawGr(self):
        if count_code!=0:
            self.get_i_rod()
            print("Fig rod")
            fig_Gr=self.newCount.makeGraf(self.i_rod)
            print("Grafishere")
            self.showGraf(fig_Gr)
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала рассчитайте конструкцию!')
            error_dialog.exec_()

    def ShowTable(self):
        if count_code != 0:
            self.get_i_rod()
            print("Table rod")
            self.get_step()
            print("Table step")
            data_ = self.newCount.makeTable(self.i_rod,self.step_rod)
            print("Tableishere")
            DialogSecondIns = TableDialogWindow(self,data_)
            DialogSecondIns.show()
            DialogSecondIns.exec()
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала рассчитайте конструкцию!')
            error_dialog.exec_()

    def showDiagram(self, fig):
        if count_code!=0:
            DialogSecondIns = EpurDialogWindow(self, fig)
            DialogSecondIns.show()
            DialogSecondIns.exec()

        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала рассчитайте конструкцию!')
            error_dialog.exec_()

    def showGraf(self, fig):
        DialogSecondIns = GrafDialogWindow(self, fig)
        DialogSecondIns.show()
        DialogSecondIns.exec()


    def GoCount(self):
        if len(json_dict)!=0:
            self.newCount.Counting_init(json_dict)
            global count_code
            count_code=1
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала сохраните файл характеристик!')
            error_dialog.exec_()

    def showConstruct(self,fig):

        DialogSecondIns = DrawDialogWindow(self, fig)
        DialogSecondIns.show()
        DialogSecondIns.exec()



    def newSter(self):

        DialogSecondIns = StergenDialogWindow(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()


    def newStop(self):

        DialogSecondIns = StoppDialogWindow(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()

    def newNoalLoad(self):

        DialogSecondIns = NodalLoadsDialogWindow(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()

    def newRodLoad(self):

        DialogSecondIns = RodLoadsDialogWindow(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False
def is_float(string):
    substring = "."
    substring2=","

    if (substring in string) or (substring2 in string):
        return True
    else:
        return False


if __name__ == '__main__':
    app=QApplication([])
    application= MainWindow()
    application.show()
    sys.exit(app.exec())