#!python3

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

# For ctrl + C to work in terminal when invoke with python ...
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class ResizeImgApp():
	def __init__(self, qapplication: QApplication) -> None:
		self.root = qapplication
		self._get_config()
		# Create threadpool for multi thread
		self.threadpool = QThreadPool()
		self.threadpool.setMaxThreadCount(MAX_THREAD_COUNT)
		self._create_main_window()


	def _create_main_window(self):
		# Main window
		self.widget = QWidget()
		# uic.loadUi(os.path.join(SCRIPT_ABS_PATH, "form.ui"), self.widget)
		# self.widget.show()
		self.ui = UI.Ui_Widget()
		self.ui.setupUi(self.widget)
		# self.widget.setGeometry(self.x, self.y, self.w, self.h)
		self.widget.closeEvent = self._closeEvent
		# input
		self._input_widgets()
		# output
		self._output_widgets()
		# image w
		self.ui.spinBox_img_width.setValue(self.config[IMAGE]["image_width"])
		# author
		self._author_widgets()
		# logo
		self._logo_widgets()
		# logo pos
		self._logo_pos()
		# Execute
		self._execute_push()

		self.widget.show()
		pass

	def _input_widgets(self):
		def browse_path():
			# cur_txt=self.ui.lineEdit_input.text()
			_dir=QFileDialog(self.widget).getExistingDirectory(None, "Open input directory...", SCRIPT_ABS_PATH, QFileDialog.Option.ShowDirsOnly)
			# pr(_dir)
			if _dir != "":
				self.ui.lineEdit_input.setText(_dir)
			# else:
				# self.ui.lineEdit_input.insert(cur_txt)

		def open_path():
			path = self.ui.lineEdit_input.text().replace("/", "\\")
			# pr(path)
			if os.path.isdir(path):
				subprocess.run(["explorer", path])
			else:
				show_err(f"Invalid path {path}")

		def reload_path():
			self.ui.lineEdit_input.setText(IN_IMG_DIR)
		# Input text
		self.ui.lineEdit_input.setText(self.config[APP]["input"])
		# Signal connect to push browse, open, reload button
		self.ui.pushButton_input_browse.clicked.connect(browse_path)
		self.ui.pushButton_input_open.clicked.connect(open_path)
		self.ui.pushButton_input_reload.clicked.connect(reload_path)
		# self.ui.
		pass

	def _output_widgets(self):
		def browse_path():
			# cur_txt=self.ui.lineEdit_output.text()
			_dir=QFileDialog(self.widget).getExistingDirectory(None,
											"Open output directory...",
											SCRIPT_ABS_PATH,
											QFileDialog.Option.ShowDirsOnly)
			# pr(_dir)
			if _dir != "":
				self.ui.lineEdit_output.setText(_dir)
			# else:
				# self.ui.lineEdit_output.insert(cur_txt)

		def open_path():
			path = self.ui.lineEdit_output.text().replace("/", "\\")
			# pr(path)
			if os.path.isdir(path):
				subprocess.run(["explorer", path])
			else:
				show_err(f"Invalid path {path}")

		def reload_path():
			self.ui.lineEdit_output.setText(OUT_IMG_DIR)

		# output text
		self.ui.lineEdit_output.setText(self.config[APP]["output"])
		# Signal connect to push browse, open, reload button
		self.ui.pushButton_output_browse.clicked.connect(browse_path)
		self.ui.pushButton_output_open.clicked.connect(open_path)
		self.ui.pushButton_output_reload.clicked.connect(reload_path)
		# self.ui.
		pass

	def _author_widgets(self):
		# Check state change
		def author_checkbox_change():
			if self.ui.checkBox_author.checkState() == Qt.CheckState.Checked:
				self.ui.lineEdit_author_name.setEnabled(True)
			else:
				self.ui.lineEdit_author_name.setEnabled(False)
		# Initial check value from config
		if self.config[AUTH][AUTH_ENABLE]:
			self.ui.checkBox_author.setCheckState(Qt.CheckState.Checked)
			self.ui.lineEdit_author_name.setEnabled(True)
		else:
			self.ui.checkBox_author.setCheckState(Qt.CheckState.Unchecked)
			self.ui.lineEdit_author_name.setEnabled(False)
		self.ui.lineEdit_author_name.setText(self.config[AUTH][AUTH_NAME])
		# Signal when check state change
		self.ui.checkBox_author.stateChanged.connect(author_checkbox_change)

	def _logo_widgets(self):
		def browse_path():
			# cur_txt=self.ui.lineEdit_output.text()
			_file=QFileDialog(self.widget).getOpenFileName(None,
											"Open logo file...",
											SCRIPT_ABS_PATH,
											"Images (*.png *.jpg *.jpeg *.tiff \
												*.tif *.bmp *.gif *.webp \
													*.nef);;All (*)")
			# pr(_file)
			if _file[0] != "":
				self.ui.lineEdit_logo_path.setText(_file[0])
		# Initial check value from config
		def logo_checkbox_change():
			state = False
			if self.ui.checkBox_logo.checkState() == Qt.CheckState.Checked:
				state = True
			# text logo path
			self.ui.lineEdit_logo_path.setEnabled(state)
			# browse logo button
			self.ui.pushButton_browse_logo.setEnabled(state)
			# label logo width
			self.ui.label_logo_width.setEnabled(state)
			# Spinbox logo width
			self.ui.spinBox_logo_width.setEnabled(state)
			# label logo pos
			self.ui.label_logo_pos.setEnabled(state)
			# combobox logo pos
			self.ui.comboBox_logo_pos.setEnabled(state)
		if self.config[LOGO]["logo_enable"]:
			self.ui.checkBox_logo.setCheckState(Qt.CheckState.Checked)
			init_state = True
		else:
			self.ui.checkBox_logo.setCheckState(Qt.CheckState.Unchecked)
			init_state = False
		self.ui.lineEdit_logo_path.setEnabled(init_state)
		self.ui.pushButton_browse_logo.setEnabled(init_state)
		self.ui.label_logo_width.setEnabled(init_state)
		self.ui.spinBox_logo_width.setEnabled(init_state)
		self.ui.label_logo_pos.setEnabled(init_state)
		self.ui.comboBox_logo_pos.setEnabled(init_state)

		self.ui.checkBox_logo.stateChanged.connect(logo_checkbox_change)
		self.ui.lineEdit_logo_path.setText(self.config[LOGO]["logo_file"])
		self.ui.pushButton_browse_logo.clicked.connect(browse_path)
		self.ui.spinBox_logo_width.setValue(self.config[LOGO]["logo_width"])
		self.ui.comboBox_logo_pos.setCurrentIndex(self.config[LOGO][POS])

		def browse_path_2():
			# cur_txt=self.ui.lineEdit_output.text()
			_file=QFileDialog(self.widget).getOpenFileName(None,
											"Open logo file...",
											SCRIPT_ABS_PATH,
											"Images (*.png *.jpg *.jpeg *.tiff \
												*.tif *.bmp *.gif *.webp \
													*.nef);;All (*)")
			# pr(_file)
			if _file[0] != "":
				self.ui.lineEdit_logo_path_2.setText(_file[0])
		# Initial check value from config
		def logo_checkbox_change_2():
			state = False
			if self.ui.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
				state = True
			# text logo path
			self.ui.lineEdit_logo_path_2.setEnabled(state)
			# browse logo button
			self.ui.pushButton_browse_logo_2.setEnabled(state)
			# label logo width
			self.ui.label_logo_width_2.setEnabled(state)
			# Spinbox logo width
			self.ui.spinBox_logo_width_2.setEnabled(state)
			# label logo pos
			self.ui.label_logo_pos_2.setEnabled(state)
			# combobox logo pos
			self.ui.comboBox_logo_pos_2.setEnabled(state)
		if self.config[LOGO_2]["logo_enable"]:
			self.ui.checkBox_logo_2.setCheckState(Qt.CheckState.Checked)
			init_state = True
		else:
			self.ui.checkBox_logo_2.setCheckState(Qt.CheckState.Unchecked)
			init_state = False
		self.ui.lineEdit_logo_path_2.setEnabled(init_state)
		self.ui.pushButton_browse_logo_2.setEnabled(init_state)
		self.ui.label_logo_width_2.setEnabled(init_state)
		self.ui.spinBox_logo_width_2.setEnabled(init_state)
		self.ui.label_logo_pos_2.setEnabled(init_state)
		self.ui.comboBox_logo_pos_2.setEnabled(init_state)

		self.ui.lineEdit_logo_path_2.setText(self.config[LOGO_2]["logo_file"])
		self.ui.spinBox_logo_width_2.setValue(self.config[LOGO_2]["logo_width"])
		self.ui.checkBox_logo_2.stateChanged.connect(logo_checkbox_change_2)
		self.ui.pushButton_browse_logo_2.clicked.connect(browse_path_2)
		self.ui.comboBox_logo_pos_2.setCurrentIndex(self.config[LOGO_2][POS])

	def _logo_pos(self):
		if DEBUG:
			pos_list=["Top Left", "Top Middle", "Top Right",
				"Left", "Middle", "Right",
				"Bottom Left", "Bottom Middle", "Bottom Right"]
			def debug_func():
				self.ui.lineEdit_DEBUG.setText(f"Logo1: {pos_list[self.ui.comboBox_logo_pos.currentIndex()]} - Logo2: {pos_list[self.ui.comboBox_logo_pos_2.currentIndex()]}")
			self.ui.comboBox_logo_pos.currentIndexChanged.connect(debug_func)
			self.ui.comboBox_logo_pos_2.currentIndexChanged.connect(debug_func)
		else:
			self.ui.lineEdit_DEBUG.hide()
		pass

	def _execute_push(self):
		def EXE():
			_aut = None
			if self.ui.checkBox_author.checkState() == Qt.CheckState.Checked:
				_aut = self.ui.lineEdit_author_name.text()
			logo_data = LogoData(None, None, None, None)
			logo_data_2 = LogoData(None, None, None, None)
			if self.ui.checkBox_logo.checkState() == Qt.CheckState.Checked:
				logo_data = LogoData(self.ui.lineEdit_logo_path.text(),
					 self.ui.spinBox_logo_width.value(),
					 None,
					 self.ui.comboBox_logo_pos.currentIndex())
			if self.ui.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
				logo_data_2 = LogoData(self.ui.lineEdit_logo_path_2.text(),
					 self.ui.spinBox_logo_width_2.value(),
					 None,
					 self.ui.comboBox_logo_pos_2.currentIndex())

			img_process = img_resize.ImageWithPIL(
				input_dir=self.ui.lineEdit_input.text(),
				output_dir=self.ui.lineEdit_output.text(),
				author_name=_aut,
				img_width=self.ui.spinBox_img_width.value(),
				logodata=logo_data,
				logodata_2=logo_data_2,
			)
			file_err = img_process.resize_all()
			if file_err:
				str_file = "File that can't be resized:"
				for file in file_err:
					str_file = str_file + "\n" + str(file)
				err = QMessageBox()
				err.setText(str_file)
				err = err.exec()

		self.ui.pushButton_EXECUTE.clicked.connect(EXE)
		pass

	def _closeEvent(self, event:QCloseEvent):
		# pr(self.ui.checkBox_author.checkState())
		# Backup and update cfg file
		try:
			name = self.ui.lineEdit_author_name.text()
			if self.ui.checkBox_author.checkState() == Qt.CheckState.Checked:
				enable_author = True
			else:
				enable_author = False
			if self.ui.checkBox_logo.checkState() == Qt.CheckState.Checked:
				enable_logo = True
			else:
				enable_logo = False
			if self.ui.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
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
					"input": self.ui.lineEdit_input.text(),
					"output": self.ui.lineEdit_output.text()
				},
				"image": {
					"image_width": self.ui.spinBox_img_width.value()
				},
				"author": [enable_author, str(name)],
				"logo": {
					"logo_enable": enable_logo,
					"logo_width": self.ui.spinBox_logo_width.value(),
					"logo_file": self.ui.lineEdit_logo_path.text(),
					"pos": self.ui.comboBox_logo_pos.currentIndex()
				},
				"logo_2": {
					"logo_enable": enable_logo_2,
					"logo_width": self.ui.spinBox_logo_width_2.value(),
					"logo_file": self.ui.lineEdit_logo_path_2.text(),
					"pos": self.ui.comboBox_logo_pos_2.currentIndex()
				}
			}
			# pr(self.ui.lineEdit_input.text())
			file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").backup_file()
			file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").update_cfg_file(cfg_dict)
		except Exception as e:
			try:
				file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").update_cfg_file(self.backup_cfg)
				pass
			except:
				pass
			show_err(e)

	def _get_config(self):
		try:
			self.config = file_ops.FileOps(SCRIPT_ABS_PATH, "cfg").get_json_data()
		except Exception as e:
			self.config = DEFAULT_CFG
			show_err(e)
		self.backup_cfg = self.config.copy()
		# app cfg
		# app_cfg=self.config[APP]
		# self.w=app_cfg[SIZE]["w"]
		# self.h=app_cfg[SIZE]["h"]
		# self.x=app_cfg[POS]["x"]
		# self.y=app_cfg[POS]["y"]
		# screen_w = self.root.primaryScreen().size().width()
		# screen_h = self.root.primaryScreen().size().height()
		# if self.w > screen_w:
		# 	self.w=screen_w
		# if self.h > screen_h:
		# 	self.h=screen_h
		# if self.x < 100:
		# 	self.x = 100
		# if self.y < 100:
		# 	self.y = 100
		# Image cfg
		self.img_width=self.config["image"]["image_width"]
		# Logo cfg
		self.logo_width=self.config["logo"]["logo_width"]

	def _start(self):
		pass


if __name__ == '__main__':
	common__init()
	app = QApplication([])
	# app.setQuitOnLastWindowClosed(False)
	rdp_win = ResizeImgApp(app)
	# rdp_win.start()
	sys.exit(app.exec())