__AUTHOR__ = "Master_lxj"
__WEBSITE__ = "http://www.dagouzi.cn"
__DOC__ = "To do something"


from PyQt5 import QtWidgets
from main import Ui_Main
from cut import Ui_Cut
import sys
import os
# from clip_image import load_images, request_ai, cut
from tset import load_images, request_ai, cut
import time


class CutWindow(QtWidgets.QMainWindow, Ui_Cut):
	
	def __init__(self, main):
		
		super(CutWindow, self).__init__()
		self.setupUi(self)
		self.main_window = main
		self.radioButton.clicked.connect(self.enable_widget)
		self.radioButton_2.clicked.connect(self.enable_widget_2)
		self.toolButton.clicked.connect(self.load_images_file)
		self.toolButton_2.clicked.connect(self.save_images_file)
		self.pushButton.clicked.connect(self.split_image)
	
	def enable_widget(self):
		
		self.widget.setEnabled(False)
		
	def enable_widget_2(self):
		
		self.widget.setEnabled(True)
		
	def load_images_file(self):
		
		load_images_file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "导入图片路径", os.path.expanduser("~"))
		if not os.path.isdir(load_images_file_path):
			if load_images_file_path:
				self.lineEdit.clear()
				QtWidgets.QMessageBox.critical(self, "路径错误", "导入的图片路径有误，请重新选择", QtWidgets.QMessageBox.Yes)
		self.lineEdit.setText(load_images_file_path)
		
	def save_images_file(self):
		
		save_images_file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "保存图片", os.path.expanduser("~"))
		if not os.path.isdir(save_images_file_path):
			if save_images_file_path:
				self.lineEdit.clear()
				QtWidgets.QMessageBox.critical(self, "路径错误", "保存路径不存在，请重新选择", QtWidgets.QMessageBox.Yes)
		self.lineEdit_2.setText(save_images_file_path)
	
	def closeEvent(self, event):
		
		reply = QtWidgets.QMessageBox.question(self, '退出', "取消裁剪?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			event.accept()
			self.main_window.show()
		else:
			event.ignore()
			
	def split_image(self):
		
		
		load_images_path = self.lineEdit.text()
		save_images_path = self.lineEdit_2.text()
		is_rect = self.radioButton_2.isChecked()
		height = self.lineEdit_4.text()
		width = self.lineEdit_5.text()
		print(width, height)
		if is_rect:
			if not height or not width:
				QtWidgets.QMessageBox.critical(self, "参数错误", "指定裁剪需要输入裁剪宽度，高度参数", QtWidgets.QMessageBox.Yes)
				return
		
		# if load_images_path and save_images_path:
		if not os.path.isdir(load_images_path) or not os.path.isdir(save_images_path):
			QtWidgets.QMessageBox.critical(self, "路径错误", "路径错误，请检查路径", QtWidgets.QMessageBox.Yes)
			return
		images = load_images(load_images_path)
		for image in images:
			i, rect = request_ai(image)
			print(i, rect)
			# print(rect)
			if not i:
				continue
			print(height)
			cut(image, save_images_path, rect, width=width, height=height)
			time.sleep(1)
			

class MainWindow(QtWidgets.QMainWindow, Ui_Main):
	
	def __init__(self):
		
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.cut_window = CutWindow(self)
		self.pushButton.clicked.connect(self.show_cut)
		
	def show_cut(self):
		
		self.cut_window.show()
		self.hide()

		
if __name__ == '__main__':
	
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
