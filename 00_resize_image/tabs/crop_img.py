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
import tools.img_crop

class CropImgApp():
	def __init__(self, config, all_tab: UI.Ui_Widget, threadpool) -> None:
		self.CROP_TAB = all_tab
		self.config = config
		# Create threadpool for multi thread
		self.threadpool = threadpool


	def start(self):
		# input
		self._input_widgets()
		# output
		self._output_widgets()
		# image w
		self.CROP_TAB.spinBox_img_width_Crop.setValue(self.config[IMAGE]["image_width"])
		self.CROP_TAB.spinBox_img_height_Crop.setValue(self.config[IMAGE]["image_height"])
		# # author
		self._author_widgets()
		# # logo
		self._logo_widgets()
		# # logo pos
		self._logo_pos()
		# # Execute
		self._execute_push()

		pass

	def _input_widgets(self):
		def browse_path():
			# cur_txt=self.CROP_TAB.lineEdit_input_Crop.text()
			_dir=QFileDialog(self.CROP_TAB.Crop_QWidget).getExistingDirectory(
				None,
				"Open input directory...",
				SCRIPT_ABS_PATH,
				QFileDialog.Option.ShowDirsOnly)
			# pr(_dir)
			if _dir != "":
				self.CROP_TAB.lineEdit_input_Crop.setText(_dir)
			# else:
				# self.CROP_TAB.lineEdit_input_Crop.insert(cur_txt)

		def open_path():
			path = self.CROP_TAB.lineEdit_input_Crop.text().replace("/", "\\")
			# pr(path)
			if os.path.isdir(path):
				subprocess.run(["explorer", path])
			else:
				show_err(f"Invalid path {path}")

		def reload_path():
			self.CROP_TAB.lineEdit_input_Crop.setText(IN_IMG_DIR)
		# Input text
		self.CROP_TAB.lineEdit_input_Crop.setText(self.config[APP]["input"])
		# Signal connect to push browse, open, reload button
		self.CROP_TAB.pushButton_input_browse_Crop.clicked.connect(browse_path)
		self.CROP_TAB.pushButton_input_open_Crop.clicked.connect(open_path)
		self.CROP_TAB.pushButton_input_reload_Crop.clicked.connect(reload_path)
		# self.CROP_TAB.
		pass

	def _output_widgets(self):
		def browse_path():
			# cur_txt=self.CROP_TAB.lineEdit_output_Crop.text()
			_dir=QFileDialog(self.CROP_TAB.Crop_QWidget).getExistingDirectory(None,
											"Open output directory...",
											SCRIPT_ABS_PATH,
											QFileDialog.Option.ShowDirsOnly)
			# pr(_dir)
			if _dir != "":
				self.CROP_TAB.lineEdit_output_Crop.setText(_dir)
			# else:
				# self.CROP_TAB.lineEdit_output_Crop.insert(cur_txt)

		def open_path():
			path = self.CROP_TAB.lineEdit_output_Crop.text().replace("/", "\\")
			# pr(path)
			if os.path.isdir(path):
				subprocess.run(["explorer", path])
			else:
				show_err(f"Invalid path {path}")

		def reload_path():
			self.CROP_TAB.lineEdit_output_Crop.setText(OUT_IMG_DIR)

		# output text
		self.CROP_TAB.lineEdit_output_Crop.setText(self.config[APP]["output"])
		# Signal connect to push browse, open, reload button
		self.CROP_TAB.pushButton_output_browse_Crop.clicked.connect(browse_path)
		self.CROP_TAB.pushButton_output_open_Crop.clicked.connect(open_path)
		self.CROP_TAB.pushButton_output_reload_Crop.clicked.connect(reload_path)
		# self.CROP_TAB.
		pass

	def _author_widgets(self):
		# Check state change
		def author_checkbox_change():
			if self.CROP_TAB.checkBox_author_Crop.checkState() == Qt.CheckState.Checked:
				self.CROP_TAB.lineEdit_author_name_Crop.setEnabled(True)
			else:
				self.CROP_TAB.lineEdit_author_name_Crop.setEnabled(False)
		# Initial check value from config
		if self.config[AUTH][AUTH_ENABLE]:
			self.CROP_TAB.checkBox_author_Crop.setCheckState(Qt.CheckState.Checked)
			self.CROP_TAB.lineEdit_author_name_Crop.setEnabled(True)
		else:
			self.CROP_TAB.checkBox_author_Crop.setCheckState(Qt.CheckState.Unchecked)
			self.CROP_TAB.lineEdit_author_name_Crop.setEnabled(False)
		self.CROP_TAB.lineEdit_author_name_Crop.setText(self.config[AUTH][AUTH_NAME])
		# Signal when check state change
		self.CROP_TAB.checkBox_author_Crop.stateChanged.connect(author_checkbox_change)

	def _logo_widgets(self):
		def browse_path():
			# cur_txt=self.CROP_TAB.lineEdit_output_Crop.text()
			_file=QFileDialog(self.CROP_TAB.Crop_QWidget).getOpenFileName(None,
											"Open logo file...",
											SCRIPT_ABS_PATH,
											"Images (*.png *.jpg *.jpeg *.tiff \
												*.tif *.bmp *.gif *.webp \
													*.nef);;All (*)")
			# pr(_file)
			if _file[0] != "":
				self.CROP_TAB.lineEdit_logo_path_Crop.setText(_file[0])
		# Initial check value from config
		def logo_checkbox_change():
			state = False
			if self.CROP_TAB.checkBox_logo.checkState() == Qt.CheckState.Checked:
				state = True
			# text logo path
			self.CROP_TAB.lineEdit_logo_path_Crop.setEnabled(state)
			# browse logo button
			self.CROP_TAB.pushButton_browse_logo_Crop.setEnabled(state)
			# label logo width
			self.CROP_TAB.label_logo_width_Crop.setEnabled(state)
			# Spinbox logo width
			self.CROP_TAB.spinBox_logo_width_Crop.setEnabled(state)
			# label logo pos
			self.CROP_TAB.label_logo_pos_Crop.setEnabled(state)
			# combobox logo pos
			self.CROP_TAB.comboBox_logo_pos_Crop.setEnabled(state)
		if self.config[LOGO]["logo_enable"]:
			self.CROP_TAB.checkBox_logo.setCheckState(Qt.CheckState.Checked)
			init_state = True
		else:
			self.CROP_TAB.checkBox_logo.setCheckState(Qt.CheckState.Unchecked)
			init_state = False
		self.CROP_TAB.lineEdit_logo_path_Crop.setEnabled(init_state)
		self.CROP_TAB.pushButton_browse_logo_Crop.setEnabled(init_state)
		self.CROP_TAB.label_logo_width_Crop.setEnabled(init_state)
		self.CROP_TAB.spinBox_logo_width_Crop.setEnabled(init_state)
		self.CROP_TAB.label_logo_pos_Crop.setEnabled(init_state)
		self.CROP_TAB.comboBox_logo_pos_Crop.setEnabled(init_state)

		self.CROP_TAB.checkBox_logo.stateChanged.connect(logo_checkbox_change)
		self.CROP_TAB.lineEdit_logo_path_Crop.setText(self.config[LOGO]["logo_file"])
		self.CROP_TAB.pushButton_browse_logo_Crop.clicked.connect(browse_path)
		self.CROP_TAB.spinBox_logo_width_Crop.setValue(self.config[LOGO]["logo_width"])
		self.CROP_TAB.comboBox_logo_pos_Crop.setCurrentIndex(self.config[LOGO][POS])

		# def browse_path_2():
		# 	# cur_txt=self.CROP_TAB.lineEdit_output_Crop.text()
		# 	_file=QFileDialog(self.CROP_TAB.Crop_QWidget).getOpenFileName(None,
		# 									"Open logo file...",
		# 									SCRIPT_ABS_PATH,
		# 									"Images (*.png *.jpg *.jpeg *.tiff \
		# 										*.tif *.bmp *.gif *.webp \
		# 											*.nef);;All (*)")
		# 	# pr(_file)
		# 	if _file[0] != "":
		# 		self.CROP_TAB.lineEdit_logo_path_2.setText(_file[0])
		# Initial check value from config
		# def logo_checkbox_change_2():
		# 	state = False
		# 	if self.CROP_TAB.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
		# 		state = True
		# 	# text logo path
		# 	self.CROP_TAB.lineEdit_logo_path_2.setEnabled(state)
		# 	# browse logo button
		# 	self.CROP_TAB.pushButton_browse_logo_2.setEnabled(state)
		# 	# label logo width
		# 	self.CROP_TAB.label_logo_width_2.setEnabled(state)
		# 	# Spinbox logo width
		# 	self.CROP_TAB.spinBox_logo_width_2.setEnabled(state)
		# 	# label logo pos
		# 	self.CROP_TAB.label_logo_pos_2.setEnabled(state)
		# 	# combobox logo pos
		# 	self.CROP_TAB.comboBox_logo_pos_2.setEnabled(state)
		# if self.config[LOGO_2]["logo_enable"]:
		# 	self.CROP_TAB.checkBox_logo_2.setCheckState(Qt.CheckState.Checked)
		# 	init_state = True
		# else:
		# 	self.CROP_TAB.checkBox_logo_2.setCheckState(Qt.CheckState.Unchecked)
		# 	init_state = False
		# self.CROP_TAB.lineEdit_logo_path_2.setEnabled(init_state)
		# self.CROP_TAB.pushButton_browse_logo_2.setEnabled(init_state)
		# self.CROP_TAB.label_logo_width_2.setEnabled(init_state)
		# self.CROP_TAB.spinBox_logo_width_2.setEnabled(init_state)
		# self.CROP_TAB.label_logo_pos_2.setEnabled(init_state)
		# self.CROP_TAB.comboBox_logo_pos_2.setEnabled(init_state)

		# self.CROP_TAB.lineEdit_logo_path_2.setText(self.config[LOGO_2]["logo_file"])
		# self.CROP_TAB.spinBox_logo_width_2.setValue(self.config[LOGO_2]["logo_width"])
		# self.CROP_TAB.checkBox_logo_2.stateChanged.connect(logo_checkbox_change_2)
		# self.CROP_TAB.pushButton_browse_logo_2.clicked.connect(browse_path_2)
		# self.CROP_TAB.comboBox_logo_pos_2.setCurrentIndex(self.config[LOGO_2][POS])

	def _logo_pos(self):
		if DEBUG:
			pos_list=["Top Left", "Top Middle", "Top Right",
				"Left", "Middle", "Right",
				"Bottom Left", "Bottom Middle", "Bottom Right"]
			def debug_func():
				self.CROP_TAB.lineEdit_DEBUG.setText(
					f"Logo1: {pos_list[self.CROP_TAB.comboBox_logo_pos_Crop.currentIndex()]} - Logo2: {pos_list[self.CROP_TAB.comboBox_logo_pos_2.currentIndex()]}")
			self.CROP_TAB.comboBox_logo_pos_Crop.currentIndexChanged.connect(debug_func)
			# self.CROP_TAB.comboBox_logo_pos_2.currentIndexChanged.connect(debug_func)
		else:
			self.CROP_TAB.lineEdit_DEBUG.hide()
		pass

	def _execute_push(self):
		def EXE():
			_aut = None
			if self.CROP_TAB.checkBox_author_Crop.checkState() == Qt.CheckState.Checked:
				_aut = self.CROP_TAB.lineEdit_author_name_Crop.text()
			logo_data = LogoData(None, None, None, None)
			# logo_data_2 = LogoData(None, None, None, None)
			if self.CROP_TAB.checkBox_logo.checkState() == Qt.CheckState.Checked:
				logo_data = LogoData(self.CROP_TAB.lineEdit_logo_path_Crop.text(),
					 self.CROP_TAB.spinBox_logo_width_Crop.value(),
					 None,
					 self.CROP_TAB.comboBox_logo_pos_Crop.currentIndex())
			# if self.CROP_TAB.checkBox_logo_2.checkState() == Qt.CheckState.Checked:
			# 	logo_data_2 = LogoData(self.CROP_TAB.lineEdit_logo_path_2.text(),
			# 		 self.CROP_TAB.spinBox_logo_width_2.value(),
			# 		 None,
			# 		 self.CROP_TAB.comboBox_logo_pos_2.currentIndex())

			img_process = tools.img_crop.ImageCropWithPIL(
				input_dir=self.CROP_TAB.lineEdit_input_Crop.text(),
				output_dir=self.CROP_TAB.lineEdit_output_Crop.text(),
				author_name=_aut,
				cfg_img_width=self.CROP_TAB.spinBox_img_width_Crop.value(),
				cfg_img_height=self.CROP_TAB.spinBox_img_height_Crop.value(),
				logodata=logo_data,
				# logodata_2=logo_data_2,
			)
			file_err = img_process.resize_all()
			if file_err:
				str_file = "File that can't be resized:"
				for file in file_err:
					str_file = str_file + "\n" + str(file)
				err = QMessageBox()
				err.setText(str_file)
				err = err.exec()

		print("Crop start")
		self.CROP_TAB.pushButton_EXECUTE_Crop.clicked.connect(EXE)
		pass

	def _start(self):
		pass
