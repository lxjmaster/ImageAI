# -*- coding: utf-8 -*-

from Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIntValidator


class ReMainWindow(Ui_MainWindow):

	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)
		# 固定窗口尺寸
		MainWindow.setFixedSize(800, 599)
		# 设置控件功能
		self.actionexit.triggered.connect(MainWindow.close)
		self.actiona.triggered.connect(self.show_about)
		self.actionhelp.triggered.connect(self.show_help)
		self.comboBox.currentIndexChanged.connect(self.clip_mode)
		self.textEdit.setAcceptDrops(False)
		self.lineEdit.setValidator(QIntValidator(15, 4096))
		self.lineEdit_2.setValidator(QIntValidator(0, 4096))

	def show_help(self):

		QMessageBox.about(
			self,
			"使用说明",
			"""
			<h2 style='text-align: center'>东莞市邦邻信息科技有限公司</h2>
			<p>东莞市邦邻信息科技有限公司成立于2006年，秉承“为中国企业打造网络营销核心竞争力”的理念，专业为中国企业特别是成长型企业提供电子商务应用解决方案和网络营销服务。</p>
			<p>于2015年取得了国家高新技术企业称号，雄厚的实力，已为20000多家企业提供了专业全面的电子商务应用和网络营销服务，并赢得了这些企业的支持和信赖。</p>
			<p>我们可以提供：营销型网站，企业网站，极速品牌网站，商城网站，微分销系统，微信系统定制开发。每一个客户都是我们唯一的客户，我们愿与您走向成功未来！</p>
			<p>官方网站：<a href='http://www.jiezanke.com/'>邦邻科技</a></p>   
			"""
		)

	def show_about(self):

		QMessageBox.about(
			self,
			"关于我们",
			"""
			<h2 style='text-align: center'>东莞市邦邻信息科技有限公司</h2>
			<p>东莞市邦邻信息科技有限公司成立于2006年，秉承“为中国企业打造网络营销核心竞争力”的理念，专业为中国企业特别是成长型企业提供电子商务应用解决方案和网络营销服务。</p>
			<p>于2015年取得了国家高新技术企业称号，雄厚的实力，已为20000多家企业提供了专业全面的电子商务应用和网络营销服务，并赢得了这些企业的支持和信赖。</p>
			<p>我们可以提供：营销型网站，企业网站，极速品牌网站，商城网站，微分销系统，微信系统定制开发。每一个客户都是我们唯一的客户，我们愿与您走向成功未来！</p>
			<p>官方网站：<a href='http://www.jiezanke.com/'>邦邻科技</a></p>   
			"""
		)

	def clip_mode(self, index):
		if index:
			self.lineEdit.setEnabled(True)
			self.lineEdit_2.setEnabled(True)
		else:
			self.lineEdit.setEnabled(False)
			self.lineEdit_2.setEnabled(False)
