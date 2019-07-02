# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:13:49 2019

@author: 赵匡是
"""

import sys;
from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtCore import *;
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTimeEdit, QPushButton;

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 209)
        self.sam_rate_label = QtWidgets.QLabel(Form)
        self.sam_rate_label.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.sam_rate_label.setObjectName("sam_rate_label")
        self.sample_rate = QtWidgets.QLineEdit(Form)
        self.sample_rate.setGeometry(QtCore.QRect(160, 20, 121, 20))
        self.sample_rate.setAlignment(QtCore.Qt.AlignCenter)
        self.sample_rate.setObjectName("sample_rate")
        self.sam_len_label = QtWidgets.QLabel(Form)
        self.sam_len_label.setGeometry(QtCore.QRect(20, 50, 91, 16))
        self.sam_len_label.setObjectName("sam_len_label")
        self.sample_length = QtWidgets.QLineEdit(Form)
        self.sample_length.setGeometry(QtCore.QRect(160, 50, 121, 20))
        self.sample_length.setAlignment(QtCore.Qt.AlignCenter)
        self.sample_length.setObjectName("sample_length")
        self.sig_len_label = QtWidgets.QLabel(Form)
        self.sig_len_label.setGeometry(QtCore.QRect(20, 80, 101, 16))
        self.sig_len_label.setObjectName("sig_len_label")
        self.signal_length = QtWidgets.QLineEdit(Form)
        self.signal_length.setGeometry(QtCore.QRect(160, 80, 121, 20))
        self.signal_length.setAlignment(QtCore.Qt.AlignCenter)
        self.signal_length.setObjectName("signal_length")
        self.frequency_resolution = QtWidgets.QLineEdit(Form)
        self.frequency_resolution.setGeometry(QtCore.QRect(160, 110, 121, 20))
        self.frequency_resolution.setAlignment(QtCore.Qt.AlignCenter)
        self.frequency_resolution.setObjectName("frequency_resolution")
        self.freq_resoluting_label = QtWidgets.QLabel(Form)
        self.freq_resoluting_label.setGeometry(QtCore.QRect(20, 110, 101, 16))
        self.freq_resoluting_label.setTextFormat(QtCore.Qt.RichText)
        self.freq_resoluting_label.setObjectName("freq_resoluting_label")
        self.freq_range_label = QtWidgets.QLabel(Form)
        self.freq_range_label.setGeometry(QtCore.QRect(20, 140, 131, 16))
        self.freq_range_label.setTextFormat(QtCore.Qt.RichText)
        self.freq_range_label.setObjectName("freq_range_label")
        self.frequency_range = QtWidgets.QLineEdit(Form)
        self.frequency_range.setGeometry(QtCore.QRect(160, 140, 121, 20))
        self.frequency_range.setAlignment(QtCore.Qt.AlignCenter)
        self.frequency_range.setObjectName("frequency_range")
        self.button_calculate = QtWidgets.QPushButton(Form)
        self.button_calculate.setGeometry(QtCore.QRect(70, 170, 75, 23))
        self.button_calculate.setObjectName("button_calculate")
        self.button_clean = QtWidgets.QPushButton(Form)
        self.button_clean.setGeometry(QtCore.QRect(150, 170, 75, 23))
        self.button_clean.setObjectName("button_clean")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DFT计算器"))
        self.sam_rate_label.setText(_translate("Form", "信号采样率(Fs)"))
        self.sam_len_label.setText(_translate("Form", "采样长度(T)"))
        self.sig_len_label.setText(_translate("Form", "样本数(N)"))
        self.freq_resoluting_label.setText(_translate("Form", "<html><head/><body><p>频率分辨率(f<span style=\" vertical-align:sub;\">0</span>)</p></body></html>"))
        self.freq_range_label.setText(_translate("Form", "<html><head/><body><p>有效频率分析范围(f<span style=\" vertical-align:sub;\">h</span>)</p></body></html>"))
        self.button_calculate.setText(_translate("Form", "计算"))
        self.button_clean.setText(_translate("Form", "清空"))

    
class Window(QWidget, Ui_Form):
    def __init__(self):
        QWidget.__init__(self);
        Ui_Form.__init__(self);
        self.setupUi(self);
        self.Fs = None;
        self.T = None;
        self.N = None;
        self.f0 = None;
        self.fh = None;
        self.sample_rate.editingFinished.connect(self.set_Fs);
        self.sample_length.editingFinished.connect(self.set_T);
        self.signal_length.editingFinished.connect(self.set_N);
        self.frequency_resolution.editingFinished.connect(self.set_f0);
        self.frequency_range.editingFinished.connect(self.set_fh);
        self.button_clean.clicked.connect(self.clean);
        
    def set_Fs(self):
        try:
            self.Fs = float(self.sample_rate.text());
            self.fh = self.Fs / 2;
            self.sample_rate.setText(str(self.Fs));
            self.frequency_range.setText(str(self.fh));
        
            if self.T is not None:
                self.N = self.Fs * self.T;
                self.signal_length.setText(str(self.N));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
                
            if self.N is not None:
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
                
            if self.f0 is not None:
                self.N = self.Fs / self.f0;
                self.signal_length.setText(str(self.N));
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
        except:
            pass;
    
    def set_T(self):
        try:
            self.T = float(self.sample_length.text());
            self.f0 = 1 / self.T;
            self.sample_length.setText(str(self.T));
            self.frequency_resolution.setText(str(self.f0));
            
            if (self.Fs is not None) or (self.fh is not None):
                self.N = self.Fs * self.T;
                self.signal_length.setText(str(self.N));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
            
            if self.N is not None:
                self.Fs = self.N / self.T;
                self.sample_rate.setText(str(self.Fs));
                self.fh = self.Fs / 2;
                self.frequency_range.setText(str(self.fh));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
        except:
            pass;
        
    def set_N(self):
        try:
            self.N = float(self.signal_length.text());
            self.signal_length.setText(str(self.N));
            
            if self.f0 is not None:
                self.Fs = self.N * self.f0;
                self.sample_rate.setText(str(self.Fs));
                self.fh = self.Fs / 2;
                self.frequency_range.setText(str(self.fh));
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
            
            if (self.Fs is not None) or (self.fh is not None):
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
                
            if self.T is not None:
                self.Fs = self.N / self.T;
                self.sample_rate.setText(str(self.Fs));
                self.fh = self.Fs / 2;
                self.frequency_range.setText(str(self.fh));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
        except:
            pass;
        
    def set_f0(self):
        try:
            self.f0 = float(self.frequency_resolution.text());
            self.T = 1 / self.f0;
            self.sample_length.setText(str(self.T));
            self.frequency_resolution.setText(str(self.f0));
            
            if self.N is not None:
                self.Fs = self.N * self.f0;
                self.sample_rate.setText(str(self.Fs));
                self.fh = self.Fs / 2;
                self.frequency_range.setText(str(self.fh));
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
            
            if self.fh is not None:
                self.N = self.Fs / self.f0;
                self.signal_length.setText(str(self.N));
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
                
            if self.Fs is not None:
                self.N = self.Fs / self.f0;
                self.signal_length.setText(str(self.N));
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
        except:
            pass;
        
    def set_fh(self):
        try:
            self.fh = float(self.frequency_range.text());
            self.Fs = self.fh * 2;
            self.sample_rate.setText(str(self.Fs));
            self.frequency_range.setText(str(self.fh));
            
            if self.f0 is not None:
                self.N = self.Fs / self.f0;
                self.signal_length.setText(str(self.N));
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
                
            if self.T is not None:
                self.N = self.Fs * self.T;
                self.signal_length.setText(str(self.N));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
                
            if self.N is not None:
                self.T = self.N / self.Fs;
                self.sample_length.setText(str(self.T));
                self.f0 = self.Fs / self.N;
                self.frequency_resolution.setText(str(self.f0));
        except:
            pass;
        
    def clean(self):
        self.Fs = None;
        self.T = None;
        self.N = None;
        self.f0 = None;
        self.fh = None;
        self.sample_rate.setText('');
        self.sample_length.setText('');
        self.signal_length.setText('');
        self.frequency_resolution.setText('');
        self.frequency_range.setText('');
            
    def click(self):
        x, y = self.mouse.position();
        self.mouse.click(x, y, 1);
        self.info('完成点击！', True);
        self.confirmButton.setEnabled(True);

if __name__ == "__main__":
    app = QApplication(sys.argv);
    window = Window();
    window.show();
    sys.exit(app.exec_());