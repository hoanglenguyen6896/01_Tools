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
from tools import file_ops

from tabs.resize_img import ResizeImgApp
from tabs.crop_img import CropImgApp

# For ctrl + C to work in terminal when invoke with python ...
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


DEFAULT_CFG_RESIZE = {
	"app": {
		"size": {
			"w": 100,
			"h": 100
		},
		"pos": {
			"x": 661,
			"y": 272
		},
		"input": os.path.join(SCRIPT_ABS_PATH, 'INPUT_DIR').replace("\\", "/"),
		"output": os.path.join(SCRIPT_ABS_PATH, 'OUTPUT_DIR').replace("\\", "/"),
	},
	"image": {
		"image_width":  IMG_DEFAULT_WIDTH
	},
	"author": [False, "Name"],
	"logo": {
		"logo_enable": False,
		"logo_width":   LOGO_DEFAULT_WIDTH,
		"logo_file": None,
		"pos": 0
	},
	"logo_2": {
		"logo_enable": False,
		"logo_width":   LOGO_DEFAULT_WIDTH,
		"logo_file": None,
		"pos": 0
	}
}

DEFAULT_CFG_CROP = {
	"app": {
		"size": {
			"w": 100,
			"h": 100
		},
		"pos": {
			"x": 661,
			"y": 272
		},
		"input": os.path.join(SCRIPT_ABS_PATH, 'INPUT_DIR').replace("\\", "/"),
		"output": os.path.join(SCRIPT_ABS_PATH, 'OUTPUT_DIR').replace("\\", "/"),
	},
	"image": {
		"image_width":  IMG_DEFAULT_CROP_WIDTH,
		"image_height":  IMG_DEFAULT_CROP_HEIGHT
	},
	"author": [False, "Name"],
	"logo": {
		"logo_enable": False,
		"logo_width":   LOGO_DEFAULT_WIDTH,
		"logo_file": None,
		"pos": 0
	},
	"logo_2": {
		"logo_enable": False,
		"logo_width":   LOGO_DEFAULT_WIDTH,
		"logo_file": None,
		"pos": 0
	}
}
class ImageApp:
	def __init__(self) -> None:
		self.widget = QWidget()
		self.all_tab = UI.Ui_Widget()
		self.all_tab.setupUi(self.widget)
		# self.widget.setGeometry(self.x, self.y, self.w, self.h)
		self.widget.closeEvent = self._closeEvent
		self._get_config()
		# Create threadpool for multi thread
		self.threadpool = QThreadPool()
		self.threadpool.setMaxThreadCount(MAX_THREAD_COUNT)

		self.widget.show()
		pass

	def _get_config(self):
		try:
			self.config_resize = file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_resize").get_json_data()
		except Exception as e:
			self.config_resize = DEFAULT_CFG_RESIZE
			show_err(e)
		self.backup_cfg_resize = self.config_resize.copy()
		try:
			self.config_crop = file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_crop").get_json_data()
		except Exception as e:
			self.config_crop = DEFAULT_CFG_CROP
			show_err(e)

		# print(self.config_crop)
		self.backup_cfg_crop = self.config_crop.copy()
		# # Image cfg
		# self.img_width_resize=self.config_resize["image"]["image_width"]
		# # Logo cfg
		# self.logo_width_resize=self.config_resize["logo"]["logo_width"]

	def _init_resize_tab(self):
		self.RESIZE_TAB = ResizeImgApp(
			config=self.config_resize, all_tab=self.all_tab, threadpool=self.threadpool)
		self.RESIZE_TAB.start()


	def _init_crop_tab(self):
		self.CROP_TAB = CropImgApp(
			config=self.config_crop, all_tab=self.all_tab, threadpool=self.threadpool)
		self.CROP_TAB.start()

	def _start(self):
		self._init_resize_tab()
		self._init_crop_tab()
		pass

	def _closeEvent(self, event:QCloseEvent):
		# pr(self.all_tab.checkBox_author.checkState())
		# Backup and update cfg file
		def resize_cfg():
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
				file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_resize").backup_file()
				file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_resize").update_cfg_file(cfg_dict)
			except Exception as e:
				try:
					file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_resize").update_cfg_file(self.backup_cfg_resize)
					pass
				except:
					pass
				show_err(e)

		def crop_cfg():
			try:
				name = self.all_tab.lineEdit_author_name_Crop.text()
				if self.all_tab.checkBox_author_Crop.checkState() == Qt.CheckState.Checked:
					enable_author = True
				else:
					enable_author = False
				if self.all_tab.checkBox_logo_Crop.checkState() == Qt.CheckState.Checked:
					enable_logo = True
				else:
					enable_logo = False
				# if self.all_tab.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
				# 	enable_logo_2 = True
				# else:
				# 	enable_logo_2 = False

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
						"input": self.all_tab.lineEdit_input_Crop.text(),
						"output": self.all_tab.lineEdit_output_Crop.text()
					},
					"image": {
						"image_width": self.all_tab.spinBox_img_width_Crop.value(),
						"image_height": self.all_tab.spinBox_img_height_Crop.value(),
					},
					"author": [enable_author, str(name)],
					"logo": {
						"logo_enable": enable_logo,
						"logo_width": self.all_tab.spinBox_logo_width_Crop.value(),
						"logo_file": self.all_tab.lineEdit_logo_path_Crop.text(),
						"pos": self.all_tab.comboBox_logo_pos_Crop.currentIndex()
					},
					# "logo_2": {
					# 	"logo_enable": enable_logo_2,
					# 	"logo_width": self.all_tab.spinBox_logo_width_2.value(),
					# 	"logo_file": self.all_tab.lineEdit_logo_path_2.text(),
					# 	"pos": self.all_tab.comboBox_logo_pos_2.currentIndex()
					# }
				}
				# print(cfg_dict)
				# pr(self.all_tab.lineEdit_input.text())
				file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_crop").backup_file()
				file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_crop").update_cfg_file(cfg_dict)
			except Exception as e:
				try:
					file_ops.FileOps(SCRIPT_ABS_PATH, "cfg_crop").update_cfg_file(self.backup_cfg_crop)
					pass
				except:
					pass
				show_err(e)

		resize_cfg()
		crop_cfg()



if __name__ == '__main__':
	common__init()
	app = QApplication([])
	# app.setQuitOnLastWindowClosed(False)
	img_app = ImageApp()
	img_app._start()
	# rdp_win.start()
	sys.exit(app.exec())