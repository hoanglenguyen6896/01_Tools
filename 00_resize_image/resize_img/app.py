#!python3

'''
pyuic6 'e:/Learning/00_Git/01_Tools/00_resize_image/resize_img/UI.ui' \
	-o \
	'e:/Learning/00_Git/01_Tools/00_resize_image/resize_img/UI.py' \
	&& \
	'e:/Learning/00_Git/01_Tools/00_resize_image/resize_img/app.py'
'''

import shutil
import subprocess
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
# from PyQt6 import uic

from common import *

import UI
import img_resize
import file_ops
import qt_thread

from tabs.resize_img import ResizeImgApp

# For ctrl + C to work in terminal when invoke with python ...
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class ImageApp:
	def __init__(self) -> None:
		self.widget = QWidget()
		self.all_tab = UI.Ui_Widget()
		self.all_tab.setupUi(self.widget)
		# self.widget.setGeometry(self.x, self.y, self.w, self.h)
		self.widget.closeEvent = self._closeEvent
		self._get_config()

		self.widget.show()
		pass

	def _get_config(self):
		try:
			self.config = file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").get_json_data()
		except Exception as e:
			self.config = DEFAULT_CFG
			show_err(e)
		self.backup_cfg = self.config.copy()
		# Image cfg
		self.img_width=self.config["image"]["image_width"]
		# Logo cfg
		self.logo_width=self.config["logo"]["logo_width"]

	def _init_resize_tab(self):
		self.RESIZE_TAB = ResizeImgApp(config=self.config, all_tab=self.all_tab)

	def _start(self):
		self._init_resize_tab()
		pass

	def _closeEvent(self, event:QCloseEvent):
		# pr(self.all_tab.checkBox_author.checkState())
		# Backup and update cfg file
		try:
			name = self.all_tab.lineEdit_author_name.text()
			if self.all_tab.checkBox_author.checkState() == Qt.CheckState.Checked:
				enable_author = True
			else:
				enable_author = False
			if self.all_tab.checkBox_logo.checkState() == Qt.CheckState.Checked:
				enable_logo = True
			else:
				enable_logo = False
			if self.all_tab.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
				enable_logo_2 = True
			else:
				enable_logo_2 = False

			cfg_dict = {
				"app": {
					"size": {
						"w": self.widget.size().width(),
						"h": self.widget.size().height()
					},
					"pos": {
						"x": self.widget.x(),
						"y": self.widget.y()
					},
					"input": self.all_tab.lineEdit_input.text(),
					"output": self.all_tab.lineEdit_output.text()
				},
				"image": {
					"image_width": self.all_tab.spinBox_img_width.value()
				},
				"author": [enable_author, str(name)],
				"logo": {
					"logo_enable": enable_logo,
					"logo_width": self.all_tab.spinBox_logo_width.value(),
					"logo_file": self.all_tab.lineEdit_logo_path.text(),
					"pos": self.all_tab.comboBox_logo_pos.currentIndex()
				},
				"logo_2": {
					"logo_enable": enable_logo_2,
					"logo_width": self.all_tab.spinBox_logo_width_2.value(),
					"logo_file": self.all_tab.lineEdit_logo_path_2.text(),
					"pos": self.all_tab.comboBox_logo_pos_2.currentIndex()
				}
			}
			# pr(self.all_tab.lineEdit_input.text())
			file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").backup_file()
			file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").update_cfg_file(cfg_dict)
		except Exception as e:
			try:
				file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").update_cfg_file(self.backup_cfg)
				pass
			except:
				pass
			show_err(e)



if __name__ == '__main__':
	common__init()
	app = QApplication([])
	# app.setQuitOnLastWindowClosed(False)
	img_app = ImageApp()
	img_app._start()
	# rdp_win.start()
	sys.exit(app.exec())