
DEBUG=False

__START_NUMBER=0

try:
	import __common
	DEBUG=True
except:
	pass

import os
import shutil

from inspect import getframeinfo, stack

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

IMG_DEFAULT_WIDTH = 750
LOGO_DEFAULT_WIDTH = 150

MAX_THREAD_COUNT=30

IMG_EXIF_DES = {
    "Title":          270,   # Title and subject encode utf-8
    "Subject":        40095, # Subject
    "Rating":         18246, # Rating1 int
    "RatingPercent":  18249, # Rating2 int
    "Keywords":       40094, # Tags encode utf-16
    "Comment":        40092, # Commentsencode utf-16
    "Author_str":     315,   # Author string encode byte
    "Author_utf16":   40093, # Author string encode utf-16
    "Copyright":      33432, # Copyright
}
SCRIPT_ABS_PATH = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

print(SCRIPT_ABS_PATH)

IN_IMG_DIR = os.path.join(SCRIPT_ABS_PATH, "INPUT_DIR").replace("\\", "/")
OUT_IMG_DIR = os.path.join(SCRIPT_ABS_PATH, "OUTPUT_DIR").replace("\\", "/")
LOGO_PATH = os.path.join(SCRIPT_ABS_PATH, "logo").replace("\\", "/")

APP="app"
SIZE="size"
POS="pos"
IMAGE="image"
LOGO="logo"
LOGO_2="logo_2"
POS="pos"
LOGO_TOP=0
LOGO_BOTTOM=1
LOGO_LEFT=0
LOGO_RIGHT=1
AUTH="author"
AUTH_ENABLE=0
AUTH_NAME=1


DEFAULT_CFG = {
	"app": {
		"size": {
			"w": 100,
			"h": 100
		},
		"pos": {
			"x": 661,
			"y": 272
		},
		"input": IN_IMG_DIR,
		"output": OUT_IMG_DIR,
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

NO_ERR = True

class LogoData:
	def __init__(self, path, width, image_data, pos):
		self.path = path
		self.width = width
		self.image_data = image_data
		self.pos = pos
		pass

def common__init():
	pr("____________________________________________________________")


""" Debug purpose """
def pr(*args):
	global __START_NUMBER
	caller = getframeinfo(stack()[1][0])
	line_info = "%s:%d " % (caller.filename, caller.lineno)
	try:
		if DEBUG:
			print(f"{__START_NUMBER}--")
			for txt in args:
				print(line_info, type(txt), txt)
			print(f"{__START_NUMBER}--")
			__START_NUMBER+=1
		else:
			with open(os.path.join(SCRIPT_ABS_PATH, "log.txt"), "a", encoding="utf-8") as log_file:
				for txt in args:
					log_file.write(str(txt))
					log_file.write("\n")
	except Exception as e:
		print("EEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRRRRRRR")
		print(e)
		print("EEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRRRRRRR")

""" Show error on a message box """
def show_err(event):
	caller = getframeinfo(stack()[1][0])
	if DEBUG:
		line_info = "%s:%d - %s" % (caller.filename, caller.lineno, event)
	else:
		line_info = str(event)
	# print(line_info)
	try:
		err = QMessageBox()
		err.setText(line_info)
		err = err.exec()
		pass
	except Exception as e:
		pr(e)
		pass

def safe_remove(_directory):
	try:
		shutil.rmtree(_directory)
		return True
	except FileNotFoundError as e:
		pr(f"[SKIP] {e}")
		return True
	except Exception as e:
		show_err(e)
		return False

def safe_mkdir(in0="", in1="", in2="", in3="", in4="", in5="", in6="", in7=""):
	try:
		os.mkdir(os.path.join(in0, in1, in2, in3, in4, in5, in6, in7))
		return True
	except Exception as e:
		show_err(e)
		return False
