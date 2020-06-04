# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.Qt import Qt
import sys
import os
from windows import ReMainWindow
import platform
import subprocess
from clip_image import request_ai, cut
import time


class ClipThread(QThread):

	output = pyqtSignal(bool, str, str)
	over = pyqtSignal()

	def __init__(self, parent=None):

		self.is_running = False
		super(ClipThread, self).__init__(parent)

	def run(self) -> None:

		self.is_running = self.parent().is_running
		image_file_path = self.parent().image_file_path
		for filename in os.listdir(image_file_path):
			if os.path.splitext(filename)[1] in [".jpg", ".png", ".bmp", ".JPG", ".PNG", ".BMP"]:
				filepath = os.path.join(image_file_path, filename)
				if self.is_running:
					try:
						self.output.emit(0, filename, "")
						status, rect = request_ai(filepath)
						if status:
							is_true, new_path = cut(
								filepath, self.parent().save_path, rect, self.parent().bg_color, self.parent().clip_width, self.parent().clip_height
							)
							self.output.emit(1, filepath, new_path)
						else:
							self.output.emit(2, filepath, rect)
					except Exception as e:
						self.output.emit(2, filepath, f"{e}")
						continue
				else:
					self.over.emit()
					return
			self.sleep(1)
		self.over.emit()

	def stop(self):

		self.is_running = False


class MainWindow(QMainWindow, ReMainWindow):

	def __init__(self, parent=None, flags=Qt.WindowFlags()):

		super(MainWindow, self).__init__(parent, flags)
		self.setupUi(self)
		self.home_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
		self.image_file_path = None
		self.get_save_path_history()
		self.bg_color = (0, 0, 0)
		self.save_path = ""
		self.clip_width = None
		self.clip_height = None
		self.image_counts = 0
		self.success_counts = 0
		self.is_running = False
		self.userPlatform = platform.system()
		self.pushButton.clicked.connect(self.load_image_files)
		self.treeWidget.itemDoubleClicked.connect(self.show_image)
		self.toolButton.clicked.connect(self.get_save_path)
		self.pushButton_2.clicked.connect(self.start_clip)
		self.clip_thread = ClipThread(self)
		self.clip_thread.output.connect(self.output_message)
		self.clip_thread.over.connect(self.over_clip)
		self.comboBox_3.activated.connect(self.update_save_item)

	def update_save_item(self):

		current_index = self.comboBox_3.currentIndex()
		with open("save_path.txt", "r+", encoding="utf8") as f:
			lines = f.readlines()
			text = lines[current_index]
			lines.append(text)
			lines.pop(current_index)
			with open("save_path.txt", "w+", encoding="utf8") as ff:
				for line in reversed(lines):
					ff.write(line)

	def format_message(self, message):

		t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

		return f"[{t}] {message}"

	def output_message(self, status, source, output):

		if status == 0:
			self.image_counts += 1
			color = "blue"
			message = self.format_message(f"<font style='color: {color};'>开始裁剪: {os.path.split(source)[1]}</font>")
		elif status == 1:
			color = "#55aa7f"
			message = self.format_message(f"<font style='color: {color};'>裁剪成功</font>")
			self.success_counts += 1
		elif status == 2:
			color = "red"
			message = self.format_message(f"<font style='color: {color};'>裁剪失败-{output}</font>")

		self.textEdit.append(message)

	def over_clip(self):

		self.pushButton_2.setText("开始裁剪")
		box = QMessageBox(
			QMessageBox.Information, "裁剪完成",
			f"共裁剪图片 {self.image_counts} 张\n成功裁剪 {self.success_counts} 张\n裁剪失败 {self.image_counts - self.success_counts}"
		)
		yes = box.addButton(self.tr("打开文件夹"), QMessageBox.YesRole)
		box.addButton(self.tr("确定"), QMessageBox.NoRole)
		box.exec_()
		if box.clickedButton() == yes:
			os.startfile(self.save_path)
		self.image_counts = 0
		self.success_counts = 0
		self.enabled()

	def get_bgcolor(self):

		index = self.comboBox_2.currentIndex()
		if index:
			return 255, 255, 255
		else:
			return 0, 0, 0

	def start_clip(self):

		if not self.image_file_path:
			QMessageBox.warning(self, "参数错误", "请导入需要裁剪的图片", QMessageBox.Ok)
			return
		if self.comboBox.currentIndex() == 1:
			if not self.lineEdit.text() or not self.lineEdit_2.text():
				QMessageBox.warning(self, "参数错误", "自定义裁剪需要设定图像尺寸", QMessageBox.Ok)
				return
			self.clip_width = int(self.lineEdit.text())
			self.clip_height = int(self.lineEdit_2.text())
		else:
			self.clip_width = None
			self.clip_height = None
		if not self.comboBox_3.currentText():
			QMessageBox.warning(self, "参数错误", "请设置图片保存路径", QMessageBox.Ok)
			return

		self.bg_color = self.get_bgcolor()
		self.save_path = self.comboBox_3.currentText()
		if not self.is_running:
			self.pushButton_2.setText("停止裁剪")
			self.is_running = not self.is_running
			self.unenable()
			self.clip_thread.start()
			self.textEdit.clear()
		else:
			self.enabled()
			self.is_running = not self.is_running
			self.clip_thread.stop()

	def enabled(self):

		self.comboBox.setEnabled(True)
		if self.comboBox.currentIndex():
			self.lineEdit.setEnabled(True)
			self.lineEdit_2.setEnabled(True)
		self.comboBox_2.setEnabled(True)
		self.comboBox_3.setEnabled(True)
		self.pushButton.setEnabled(True)
		self.toolButton.setEnabled(True)
		self.is_running = not self.is_running

	def unenable(self):

		self.lineEdit.setEnabled(False)
		self.lineEdit_2.setEnabled(False)
		self.comboBox.setEnabled(False)
		self.comboBox_2.setEnabled(False)
		self.comboBox_3.setEnabled(False)
		self.pushButton.setEnabled(False)
		self.toolButton.setEnabled(False)

	def get_save_path_history(self):

		if os.path.exists("save_path.txt"):
			with open("save_path.txt", "r+", encoding="utf8") as f:
				lines = f.readlines()
				if len(lines) > 5:
					with open("save_path.txt", "w+", encoding="utf8") as ff:
						for line in lines[-5:]:
							ff.write(line)
		else:
			with open("save_path.txt", "w+", encoding="utf8"):
				pass
		with open("save_path.txt", "r+", encoding="utf8") as fff:
			for index, line in enumerate(fff.readlines()):
				self.comboBox_3.insertItem(index, line.strip())

	def get_save_path(self):

		save_path = QFileDialog.getExistingDirectory(self, "选择图片保存路径", self.home_path)
		if save_path:
			self.comboBox_3.insertItem(0, save_path)
			self.comboBox_3.setCurrentIndex(0)
			with open("save_path.txt", "a+", encoding="utf8") as f:
				f.write(save_path+"\n")

	def show_image(self, item, column):

		text = item.text(0)
		file_name = os.path.join(self.image_file_path, text)
		if os.path.isfile(file_name):
			if self.userPlatform == 'Darwin':  # Mac
				subprocess.call(['open', file_name])
			elif self.userPlatform == 'Linux':  # Linux
				subprocess.call(['xdg-open', file_name])
			else:  # Windows
				os.startfile(file_name)

	def load_image_files(self):

		image_file_path = QFileDialog.getExistingDirectory(self, "选择导入的图片文件夹", self.home_path)
		if image_file_path:
			self.image_file_path = image_file_path
			self.set_file_tree()

	def set_file_tree(self):

		self.treeWidget.clear()
		root_name = os.path.basename(self.image_file_path)
		root = QTreeWidgetItem(self.treeWidget)
		root.setText(0, root_name)
		root.setIcon(0, QIcon("images/folder.png"))
		for filename in os.listdir(self.image_file_path):
			if os.path.splitext(filename)[1] in [".jpg", ".png", ".bmp", ".JPG", ".PNG", ".BMP"]:
				# self.image_counts += 1
				child = QTreeWidgetItem(root)
				child.setText(0, filename)
				child.setIcon(0, QIcon("images/picture.png"))
		self.treeWidget.expandAll()
		# for dirpath, dirnames, filenames in os.walk(self.image_file_path):
		# 	level = dirpath.replace(self.image_file_path, "").count(os.sep)
		# 	if level:
		# 		child_root = QTreeWidgetItem(root)
		# 		child_root.setText(0, os.path.basename(dirpath))
		# 		child_root.setIcon(0, QIcon("images/folder.png"))
		# 		for filename in filenames:
		# 			child = QTreeWidgetItem(child_root)
		# 			child.setText(0, filename)
		# 			child.setIcon(0, QIcon("images/picture.png"))
		# 		# for dirname in dirnames:
		# 		# 	child_root = QTreeWidgetItem(root)
		# 		# 	child_root.setText(0, dirname)
		# 		# 	child_root.setIcon(0, QIcon("images/folder.png"))
		# 	else:
		# 		for filename in filenames:
		# 			child = QTreeWidgetItem(root)
		# 			child.setText(0, filename)
		# 			child.setIcon(0, QIcon("images/picture.png"))


if __name__ == "__main__":

	app = QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())
