# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from mainwindowmlhf import Ui_MainWindow
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMessageBox  # QmessageBox是弹出框函数
import numpy as np
import xgboost as xgb

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=16, height=10, dpi=100, number =1):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("#F5F5F5") # 背景色

        fig.subplots_adjust(left=0.12, top=0.92, right=0.95, bottom=0.15) # Margins

        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.new = Ui_MainWindow()
        self.new.setupUi(self)

        self.new.lineEdit.setText('0.5')
        self.new.lineEdit_2.setText('4.98')
        self.new.lineEdit_3.setText('650')

        l = QtWidgets.QVBoxLayout(self.new.widget)
        #self.sc = MyMplCanvas(self.new.widget, width=5, height=4, dpi=100)
        self.sc = MyMplCanvas(self.new.widget, dpi=100)
        l.addWidget(self.sc)

        # #TAB2 界面函数响应
        self.new.pushButton.clicked.connect(self.plotChangeHistory)   #槽函数不用加括号
        self.new.pushButton_2.clicked.connect(self.saveResult)   #槽函数不用加括号


##################################################################
###################开始定义类内部函数#############################
##################################################################


    def plotChangeHistory(self):
        plt = self.sc  # 创建图表1
        plt.axes.cla()

        X = np.arange(-30.8, 60.2, 1.4)
        Y = np.arange(10, -12, -2)

        self.model = xgb.Booster(model_file='ImpingingJet.model')


        Speed = self.new.lineEdit.text()
        FlowVelocity = self.new.lineEdit_2.text()
        Temperature = self.new.lineEdit_3.text()

        try:
            Speed, FlowVelocity, Temperature = float(Speed), float(FlowVelocity), float(Temperature)
        except:

            print('Please make sure that the contents of the three input boxes are not empty!')
            # messagebox.showinfo(title="Error",
            #                     message="Please make sure that the contents of the three input boxes are not empty!")
            return

        INPUT = []
        for y in Y:
            for x in X:
                INPUT.append([x, abs(y), Speed, FlowVelocity, Temperature])
        self.data = pd.DataFrame(data=INPUT, columns=["x", "y", "Speed", "Velocity", "Temperature"])
        INPUT = xgb.DMatrix(np.array(INPUT))
        OUTPUT = self.model.predict(INPUT)
        self.data["HF"] = OUTPUT
        xs, ys, zs = [], [], []
        i = 0
        for y in Y:
            xs.append(X)
            ys.append([y for _ in range(len(X))])
            zs.append(OUTPUT[i * len(X):(i + 1) * len(X)])
            i += 1
        xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)
        plt.axes.contourf(xs, ys, zs, 10, cmap="YlOrRd", alpha=1)

        #plt.axes.scatter(indexNo, Para)

        # plt.xlabel("x")
        # plt.ylabel("y")
        #
        #
        # '''
        # for i in range(len(indexNo)):
        #     plt.axes.text(indexNo[i], Para[i] ,stripID[i], family='serif', style='italic', ha='right', wrap=True)
        # '''

        plt.axes.set_xlabel('X (mm)')
        plt.axes.set_ylabel('Y (mm)')
        plt.draw()

    def saveResult(self):
        self.data.to_csv('result.csv', index=False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
