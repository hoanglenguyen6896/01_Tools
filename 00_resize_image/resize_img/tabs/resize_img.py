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

class ResizeImgApp():
	def __init__(self, config, all_tab: UI.Ui_Widget) -> None:
		self.RESIZE_TAB = all_tab
		self.config = config
		# Create threadpool for multi thread
		self.threadpool = QThreadPool()
		self.threadpool.setMaxThreadCount(MAX_THREAD_COUNT)
		self._create_main_window()


	def _create_main_window(self):
		# input
		self._input_widgets()
		# output
		self._output_widgets()
		# image w
		self.RESIZE_TAB.spinBox_img_width.setValue(self.config[IMAGE]["image_width"])
		# author
		self._author_widgets()
		# logo
		self._logo_widgets()
		# logo pos
		self._logo_pos()
		# Execute
		self._execute_push()

		pass

	def _input_widgets(self):
		def browse_path():
			# cur_txt=self.RESIZE_TAB.lineEdit_input.text()
			_dir=QFileDialog(self.RESIZE_TAB.Resize_QWidget).getExistingDirectory(
				None,
				"Open input directory...",
				SCRIPT_ABS_PATH,
				QFileDialog.Option.ShowDirsOnly)
			# pr(_dir)
			if _dir != "":
				self.RESIZE_TAB.lineEdit_input.setText(_dir)
			# else:
				# self.RESIZE_TAB.lineEdit_input.insert(cur_txt)

		def open_path():
			path = self.RESIZE_TAB.lineEdit_input.text().replace("/", "\\")
			# pr(path)
			if os.path.isdir(path):
				subprocess.run(["explorer", path])
			else:
				show_err(f"Invalid path {path}")

		def reload_path():
			self.RESIZE_TAB.lineEdit_input.setText(IN_IMG_DIR)
		# Input text
		self.RESIZE_TAB.lineEdit_input.setText(self.config[APP]["input"])
		# Signal connect to push browse, open, reload button
		self.RESIZE_TAB.pushButton_input_browse.clicked.connect(browse_path)
		self.RESIZE_TAB.pushButton_input_open.clicked.connect(open_path)
		self.RESIZE_TAB.pushButton_input_reload.clicked.connect(reload_path)
		# self.RESIZE_TAB.
		pass

	def _output_widgets(self):
		def browse_path():
			# cur_txt=self.RESIZE_TAB.lineEdit_output.text()
			_dir=QFileDialog(self.RESIZE_TAB.Resize_QWidget).getExistingDirectory(None,
											"Open output directory...",
											SCRIPT_ABS_PATH,
											QFileDialog.Option.ShowDirsOnly)
			# pr(_dir)
			if _dir != "":
				self.RESIZE_TAB.lineEdit_output.setText(_dir)
			# else:
				# self.RESIZE_TAB.lineEdit_output.insert(cur_txt)

		def open_path():
			path = self.RESIZE_TAB.lineEdit_output.text().replace("/", "\\")
			# pr(path)
			if os.path.isdir(path):
				subprocess.run(["explorer", path])
			else:
				show_err(f"Invalid path {path}")

		def reload_path():
			self.RESIZE_TAB.lineEdit_output.setText(OUT_IMG_DIR)

		# output text
		self.RESIZE_TAB.lineEdit_output.setText(self.config[APP]["output"])
		# Signal connect to push browse, open, reload button
		self.RESIZE_TAB.pushButton_output_browse.clicked.connect(browse_path)
		self.RESIZE_TAB.pushButton_output_open.clicked.connect(open_path)
		self.RESIZE_TAB.pushButton_output_reload.clicked.connect(reload_path)
		# self.RESIZE_TAB.
		pass

	def _author_widgets(self):
		# Check state change
		def author_checkbox_change():
			if self.RESIZE_TAB.checkBox_author.checkState() == Qt.CheckState.Checked:
				self.RESIZE_TAB.lineEdit_author_name.setEnabled(True)
			else:
				self.RESIZE_TAB.lineEdit_author_name.setEnabled(False)
		# Initial check value from config
		if self.config[AUTH][AUTH_ENABLE]:
			self.RESIZE_TAB.checkBox_author.setCheckState(Qt.CheckState.Checked)
			self.RESIZE_TAB.lineEdit_author_name.setEnabled(True)
		else:
			self.RESIZE_TAB.checkBox_author.setCheckState(Qt.CheckState.Unchecked)
			self.RESIZE_TAB.lineEdit_author_name.setEnabled(False)
		self.RESIZE_TAB.lineEdit_author_name.setText(self.config[AUTH][AUTH_NAME])
		# Signal when check state change
		self.RESIZE_TAB.checkBox_author.stateChanged.connect(author_checkbox_change)

	def _logo_widgets(self):
		def browse_path():
			# cur_txt=self.RESIZE_TAB.lineEdit_output.text()
			_file=QFileDialog(self.RESIZE_TAB.Resize_QWidget).getOpenFileName(None,
											"Open logo file...",
											SCRIPT_ABS_PATH,
											"Images (*.png *.jpg *.jpeg *.tiff \
												*.tif *.bmp *.gif *.webp \
													*.nef);;All (*)")
			# pr(_file)
			if _file[0] != "":
				self.RESIZE_TAB.lineEdit_logo_path.setText(_file[0])
		# Initial check value from config
		def logo_checkbox_change():
			state = False
			if self.RESIZE_TAB.checkBox_logo.checkState() == Qt.CheckState.Checked:
				state = True
			# text logo path
			self.RESIZE_TAB.lineEdit_logo_path.setEnabled(state)
			# browse logo button
			self.RESIZE_TAB.pushButton_browse_logo.setEnabled(state)
			# label logo width
			self.RESIZE_TAB.label_logo_width.setEnabled(state)
			# Spinbox logo width
			self.RESIZE_TAB.spinBox_logo_width.setEnabled(state)
			# label logo pos
			self.RESIZE_TAB.label_logo_pos.setEnabled(state)
			# combobox logo pos
			self.RESIZE_TAB.comboBox_logo_pos.setEnabled(state)
		if self.config[LOGO]["logo_enable"]:
			self.RESIZE_TAB.checkBox_logo.setCheckState(Qt.CheckState.Checked)
			init_state = True
		else:
			self.RESIZE_TAB.checkBox_logo.setCheckState(Qt.CheckState.Unchecked)
			init_state = False
		self.RESIZE_TAB.lineEdit_logo_path.setEnabled(init_state)
		self.RESIZE_TAB.pushButton_browse_logo.setEnabled(init_state)
		self.RESIZE_TAB.label_logo_width.setEnabled(init_state)
		self.RESIZE_TAB.spinBox_logo_width.setEnabled(init_state)
		self.RESIZE_TAB.label_logo_pos.setEnabled(init_state)
		self.RESIZE_TAB.comboBox_logo_pos.setEnabled(init_state)

		self.RESIZE_TAB.checkBox_logo.stateChanged.connect(logo_checkbox_change)
		self.RESIZE_TAB.lineEdit_logo_path.setText(self.config[LOGO]["logo_file"])
		self.RESIZE_TAB.pushButton_browse_logo.clicked.connect(browse_path)
		self.RESIZE_TAB.spinBox_logo_width.setValue(self.config[LOGO]["logo_width"])
		self.RESIZE_TAB.comboBox_logo_pos.setCurrentIndex(self.config[LOGO][POS])

		def browse_path_2():
			# cur_txt=self.RESIZE_TAB.lineEdit_output.text()
			_file=QFileDialog(self.RESIZE_TAB.Resize_QWidget).getOpenFileName(None,
											"Open logo file...",
											SCRIPT_ABS_PATH,
											"Images (*.png *.jpg *.jpeg *.tiff \
												*.tif *.bmp *.gif *.webp \
													*.nef);;All (*)")
			# pr(_file)
			if _file[0] != "":
				self.RESIZE_TAB.lineEdit_logo_path_2.setText(_file[0])
		# Initial check value from config
		def logo_checkbox_change_2():
			state = False
			if self.RESIZE_TAB.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
				state = True
			# text logo path
			self.RESIZE_TAB.lineEdit_logo_path_2.setEnabled(state)
			# browse logo button
			self.RESIZE_TAB.pushButton_browse_logo_2.setEnabled(state)
			# label logo width
			self.RESIZE_TAB.label_logo_width_2.setEnabled(state)
			# Spinbox logo width
			self.RESIZE_TAB.spinBox_logo_width_2.setEnabled(state)
			# label logo pos
			self.RESIZE_TAB.label_logo_pos_2.setEnabled(state)
			# combobox logo pos
			self.RESIZE_TAB.comboBox_logo_pos_2.setEnabled(state)
		if self.config[LOGO_2]["logo_enable"]:
			self.RESIZE_TAB.checkBox_logo_2.setCheckState(Qt.CheckState.Checked)
			init_state = True
		else:
			self.RESIZE_TAB.checkBox_logo_2.setCheckState(Qt.CheckState.Unchecked)
			init_state = False
		self.RESIZE_TAB.lineEdit_logo_path_2.setEnabled(init_state)
		self.RESIZE_TAB.pushButton_browse_logo_2.setEnabled(init_state)
		self.RESIZE_TAB.label_logo_width_2.setEnabled(init_state)
		self.RESIZE_TAB.spinBox_logo_width_2.setEnabled(init_state)
		self.RESIZE_TAB.label_logo_pos_2.setEnabled(init_state)
		self.RESIZE_TAB.comboBox_logo_pos_2.setEnabled(init_state)

		self.RESIZE_TAB.lineEdit_logo_path_2.setText(self.config[LOGO_2]["logo_file"])
		self.RESIZE_TAB.spinBox_logo_width_2.setValue(self.config[LOGO_2]["logo_width"])
		self.RESIZE_TAB.checkBox_logo_2.stateChanged.connect(logo_checkbox_change_2)
		self.RESIZE_TAB.pushButton_browse_logo_2.clicked.connect(browse_path_2)
		self.RESIZE_TAB.comboBox_logo_pos_2.setCurrentIndex(self.config[LOGO_2][POS])

	def _logo_pos(self):
		if DEBUG:
			pos_list=["Top Left", "Top Middle", "Top Right",
				"Left", "Middle", "Right",
				"Bottom Left", "Bottom Middle", "Bottom Right"]
			def debug_func():
				self.RESIZE_TAB.lineEdit_DEBUG.setText(
					f"Logo1: {pos_list[self.RESIZE_TAB.comboBox_logo_pos.currentIndex()]} - Logo2: {pos_list[self.RESIZE_TAB.comboBox_logo_pos_2.currentIndex()]}")
			self.RESIZE_TAB.comboBox_logo_pos.currentIndexChanged.connect(debug_func)
			self.RESIZE_TAB.comboBox_logo_pos_2.currentIndexChanged.connect(debug_func)
		else:
			self.RESIZE_TAB.lineEdit_DEBUG.hide()
		pass

	def _execute_push(self):
		def EXE():
			_aut = None
			if self.RESIZE_TAB.checkBox_author.checkState() == Qt.CheckState.Checked:
				_aut = self.RESIZE_TAB.lineEdit_author_name.text()
			logo_data = LogoData(None, None, None, None)
			logo_data_2 = LogoData(None, None, None, None)
			if self.RESIZE_TAB.checkBox_logo.checkState() == Qt.CheckState.Checked:
				logo_data = LogoData(self.RESIZE_TAB.lineEdit_logo_path.text(),
					 self.RESIZE_TAB.spinBox_logo_width.value(),
					 None,
					 self.RESIZE_TAB.comboBox_logo_pos.currentIndex())
			if self.RESIZE_TAB.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
				logo_data_2 = LogoData(self.RESIZE_TAB.lineEdit_logo_path_2.text(),
					 self.RESIZE_TAB.spinBox_logo_width_2.value(),
					 None,
					 self.RESIZE_TAB.comboBox_logo_pos_2.currentIndex())

			img_process = img_resize.ImageWithPIL(
				input_dir=self.RESIZE_TAB.lineEdit_input.text(),
				output_dir=self.RESIZE_TAB.lineEdit_output.text(),
				author_name=_aut,
				img_width=self.RESIZE_TAB.spinBox_img_width.value(),
				logodata=logo_data,
				logodata_2=logo_data_2,
			)
			return
			file_err = img_process.resize_all()
			if file_err:
				str_file = "File that can't be resized:"
				for file in file_err:
					str_file = str_file + "\n" + str(file)
				err = QMessageBox()
				err.setText(str_file)
				err = err.exec()

		self.RESIZE_TAB.pushButton_EXECUTE.clicked.connect(EXE)
		pass

	def _start(self):
		pass
