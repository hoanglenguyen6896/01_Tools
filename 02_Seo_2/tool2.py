"""
HOW TO USE
1. Prepare the text
- On mysapo, upload all the image at once, so that all the image on 1 line in
the HTML format. The image should already arranged in order it should appear in
the docs
- All picture should not be separate by anything:
Example of a valid data:
	<p dir="ltr" style="text-align: center;"><img data-thumb="original" original-height="500" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-1.jpg?v=1694781355055" /><img data-thumb="original" original-height="747" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-2.jpg?v=1694781355826" /><img data-thumb="original" original-height="938" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-3.jpg?v=1694781357250" /></p>

	or

	<p dir="ltr" style="text-align: center;"><img data-thumb="original" original-height="500" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-1.jpg?v=1694781355055" /><img data-thumb="original" original-height="747" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-2.jpg?v=1694781355826" /><img data-thumb="original" original-height="938" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-3.jpg?v=1694781357250" /></p>
	<p dir="ltr" style="text-align: center;"><img data-thumb="original" original-height="500" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-1.jpg?v=1694781355055" /><img data-thumb="original" original-height="747" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-2.jpg?v=1694781355826" /><img data-thumb="original" original-height="938" original-width="750" src="//bizweb.dktcdn.net/100/438/408/files/hypebeast-la-gi-3.jpg?v=1694781357250" /></p>
- The place where you want to put the picture, the text/docs format should contain:
		- "rrr"
	or if in html format, it should be one of these:
		- <p dir="ltr">rrr</p>
		- <p>rrr</p>
	If you want to change the "rrr" pattern, modify the variable **replace_pattern** below in the code

2. Use the tool:
	1. Open any terminal that support running python and navigate to folder contain tool.py
	2. Put the RAW HTML format in to IN.html
	3. Run tool:
		python <path/to/tool.py>
	After that you can get HTML format in OUT.html, paste it to your sapo html format


"""

DEBUG=False
import sys

import colorama
from colorama import Fore
colorama.init(autoreset = True)

PRINT_COLOR = {
	"ERROR":		Fore.RED,
	"WARNING":		Fore.YELLOW,
}

import re

import difflib
from difflib import SequenceMatcher
def get_similarity_ratio(check_str, key_str):
	if len(check_str.split(" ")) > 5:
		return 0.55
	tmp = 0
	for _w in check_str.split(" "):
		if _w.lower() in key_str.lower():
			tmp += 1
	return (tmp/len(key_str.split(" ")))


input_file = ""

target_line=""

text_align_center="<p dir=\"ltr\" style=\"text-align: center;\">"
img_txt_replace="<img data-thumb="
img_txt_to="<img alt=\"REPLACE_HEADER\" data-thumb="
picture_comment="<p dir=\"ltr\" style=\"text-align: center;\"><em>REPLACE_HEADER</em></p>"

# PARTERN to check replace
replace_pattern = "rrr"
# replace_pattern=["<p>rrr</p>", "<p dir=\"ltr\">rrr</p>"]

havelink = "</a>"

LINK_PRT = "<a"
LINK_PRT_REPLACE = "<strong><span style=\"color: #ed1c24;\"><a style=\"color: #ed1c24;\""

# Header pattern
hdr_pattern = ["</h1>", "</h2>", "</h3>"]

TXT_FOR_REPLACEMENT="REPLACE_HEADER"

HEADER_DEFALT = "IMAGE_NEEDS_TO_BE_CHECKKKKKKKKKKKKKKKKKKKKKKKKED"
HEADER = HEADER_DEFALT
HEADER_TEXT = HEADER_DEFALT
TMP_HEADER = ""

PRIMARY_KEY=""

PATTERN_TO_GET_IMG_LINE = "[caption id=\"attachment_"
PATTERN_ALT = "alt=\"\""
PATTERN_ALT_REPLACE = f"alt=\"{TXT_FOR_REPLACEMENT}\""


NEW_ALT = ""
HEADER_REGEX = re.compile(r";\">\w*\S+")
PRT_HDR_SIZE = "__SIZE"
PRT_HDR_NUM = "__REPNUM"
PATTERN_HEADER_AND_SIZE = f"<span style=\"font-size: {PRT_HDR_SIZE}%; color: #00aae7;\">{PRT_HDR_NUM}</span>"


# List image line
IMG_TXT_INFO=[]
# List comment line
IMG_CMT_INFO=[]
# Current line
CURR_LINE = 0

def write_img_back(_file, _idx):
	global TMP_HEADER
	global CURR_LINE
	global PRIMARY_KEY
	CURR_LINE += 1
	_file.writelines(text_align_center)
	# Replace alt
	if get_similarity_ratio(HEADER_TEXT, PRIMARY_KEY) < 0.5:
		_file.writelines(IMG_TXT_INFO[_idx].replace(TXT_FOR_REPLACEMENT, PRIMARY_KEY))
	else:
		_file.writelines(IMG_TXT_INFO[_idx].replace(TXT_FOR_REPLACEMENT, HEADER_TEXT))
	_file.writelines("\n")
	CURR_LINE += 1
	# Replace comment
	_file.writelines(IMG_CMT_INFO[_idx].replace(TXT_FOR_REPLACEMENT,HEADER_TEXT))
	_file.writelines("\n")
	if (TMP_HEADER == HEADER_TEXT):
		print(PRINT_COLOR["WARNING"] + "WARNING: 2 picture has same comment and attribute")
		print(f"\tPlz check line {CURR_LINE - 1}")
	TMP_HEADER = HEADER_TEXT


def dbg_init(data_str = ""):
	global DEBUG
	if DEBUG==True:
		with open("tmp.html", \
							"w", \
							encoding="utf-8") \
		as out_file:
			pass
	pass

def dbg_append(data_str = ""):
	global DEBUG
	if DEBUG==True:
		with open("tmp.html", \
							"a", \
							encoding="utf-8") \
		as out_file:
			out_file.writelines(str(data_str) + "\n")
	pass

"""
Get file data
"""
def get_file_data(path):
	with open(path, "r", encoding="utf-8") as f:
		input_file = f.readlines()
	return input_file


"""
Get header content
Remove 1. 2. from it
"""
def get_header(_txt):
	global HEADER
	global HEADER_TEXT
	for patt in hdr_pattern:
		if patt in _txt:
			HEADER = patt[2:-1]
			_HEADER_TEXT = _txt.replace(f"<{HEADER} dir=\"ltr\">","").\
										replace(f"</{HEADER}>","").split(" ")
			if (len(_HEADER_TEXT) > 1):
				_HEADER_TEXT = _HEADER_TEXT[1:]
			HEADER_TEXT = " ".join(_HEADER_TEXT).replace("\n","")

def coloring_bigger_header(data_str):
	tmp = re.findall(HEADER_REGEX, data_str)
	if len(tmp) != 1:
		return False
	hdr_txt = tmp[0][3:]
	header_content = data_str.split(hdr_txt)
	print(header_content)
	list_hdr_txt = [x for x in hdr_txt]
	dots = sum(c == "." for c in hdr_txt)
	htype = len(list_hdr_txt) - dots + 1
	if htype == 2:
		size = "150"
	else:
		size = "130"
	_tmp_str = data_str
	return _tmp_str

def link_handle(data_str):
	href_pattern = re.compile(r'href="(?:[^"]|"")*"', re.IGNORECASE)
	href_str = re.findall(href_pattern, data_str)
	_str = href_str[0] + "><span style=\"font-weight: 400;\">"
	_str2 = href_str[0] + " target=\"_blank\" rel=\"noopener\">"
	# print(_str, _str2)
	_tmp_str = data_str.replace(_str, _str2)\
						.replace(LINK_PRT, LINK_PRT_REPLACE).replace("</a>", "</a></strong>")
	return _tmp_str

def bold_spec_name(data_str):
	_tmp_str = data_str.replace("1102 STYLE", "<strong>1102 STYLE</strong>")\
				.replace("Hàng Hiệu Siêu Cấp","<strong>Hàng Hiệu Siêu Cấp</strong>")
	return _tmp_str
	pass

def image_process(data_str):
	comment_img = data_str.split("\" /> ")[1].split("[/caption]")[0]
	# print(HEADER_TEXT)
	NEW_ALT = HEADER_TEXT.split(";\">")[1].split(" ")[1:]
	NEW_ALT = " ".join(NEW_ALT).split("</")[0]
	print(NEW_ALT)
	if get_similarity_ratio(NEW_ALT, PRIMARY_KEY) < 0.5:
		_tmp_str = data_str.replace(comment_img, f"{NEW_ALT} - {PRIMARY_KEY}").replace(PATTERN_ALT, \
								PATTERN_ALT_REPLACE.replace(\
									TXT_FOR_REPLACEMENT, f"{NEW_ALT} - {PRIMARY_KEY}"))
	else:
		_tmp_str = data_str.replace(comment_img, NEW_ALT).replace(PATTERN_ALT, \
								PATTERN_ALT_REPLACE.replace(\
									TXT_FOR_REPLACEMENT, NEW_ALT))
	return _tmp_str

if __name__ == "__main__":
	dbg_init()

	if len(sys.argv) <= 1:
		# print(PRINT_COLOR["ERROR"] + "ERROR: No primary key")
		exit()
	else:
		PRIMARY_KEY = " ".join(sys.argv[1:])

	file_content = get_file_data("IN.html")

	for _line in file_content:
		# print(_line)
		if(PATTERN_TO_GET_IMG_LINE in _line):
			IMG_TXT_INFO.append(_line.replace(PATTERN_ALT, \
								PATTERN_ALT_REPLACE.replace(\
									TXT_FOR_REPLACEMENT, PRIMARY_KEY)))

	IMG_CMT_INFO=[picture_comment]*(len(IMG_TXT_INFO))

	write_idx = 0
	continue_upper = 0
	with open("OUT.html", \
						"w", \
						encoding="utf-8") \
	as out_file:
		line_CINK = ""
		file_rev = file_content.copy()
		file_rev.reverse()
		for rev_line in file_rev:
			if "DR CINK" in rev_line:
				line_CINK = rev_line
				break
		first_focus = 0
		for _line in file_content:
			# if (PRIMARY_KEY in _line) and (first_focus == 0):
			# 	first_focus == 1
			# 	_line = _line.replace()
			for hrdcheck in hdr_pattern:
				if hrdcheck in _line:
					get_header(_line)
					# _line_tmp = coloring_bigger_header(_line)
					# _line_tmp2 = bold_spec_name(_line_tmp)
					out_file.writelines(_line)
					continue_upper = 1
					break
			if havelink in _line:
				# _line_tmp = link_handle(_line)
				# _line_tmp2 = bold_spec_name(_line_tmp)
				out_file.writelines(_line)
				continue_upper = 1
			if continue_upper == 1:
				continue_upper = 0
				continue

			if PATTERN_TO_GET_IMG_LINE in _line:
				continue
			if replace_pattern in _line:
				out_file.writelines(image_process(IMG_TXT_INFO[write_idx]))
				write_idx += 1
			else:
				CURR_LINE += 1
				# _line_tmp2 = bold_spec_name(_line)
				if line_CINK == _line:
					out_file.writelines(_line.replace("DR CINK", "<a href=\"https://drcink.com.vn/\"><span style=\"color: #ed1c24;\"><strong>DR CINK</strong></span></a>"))
				else:
					out_file.writelines(_line)
		if write_idx != len(IMG_CMT_INFO):
			print("Errrrrrrrrrrrr")
	print(sys.argv)