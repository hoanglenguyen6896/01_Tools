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

import sys

import colorama
from colorama import Fore
colorama.init(autoreset = True)

PRINT_COLOR = {
	"ERROR":		Fore.RED,
	"WARNING":		Fore.YELLOW,
}

import difflib
from difflib import SequenceMatcher
def get_similarity_ratio(check_str, key_str):
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

# Header pattern
hdr_pattern = ["</h1>", "</h2>", "</h3>"]


format_cmt_existed = 1
next_line_will_be_comment = 0

REPLACE_TEXT_IMG="REPLACE_HEADER"

HEADER_DEFALT = "IMAGE_NEEDS_TO_BE_CHECKKKKKKKKKKKKKKKKKKKKKKKKED"
HEADER = HEADER_DEFALT
HEADER_TEXT = HEADER_DEFALT
TMP_HEADER = ""

PRIMARY_KEY=""

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
	global format_cmt_existed
	global next_line_will_be_comment
	CURR_LINE += 1
	_file.writelines(text_align_center)
	# Replace alt
	if get_similarity_ratio(HEADER_TEXT, PRIMARY_KEY) < 0.5:
		_file.writelines(IMG_TXT_INFO[_idx].replace(REPLACE_TEXT_IMG, PRIMARY_KEY))
	else:
		_file.writelines(IMG_TXT_INFO[_idx].replace(REPLACE_TEXT_IMG, HEADER_TEXT))
	_file.writelines("\n")
	CURR_LINE += 1
	# Replace comment
	if format_cmt_existed == 0:
		_file.writelines(IMG_CMT_INFO[_idx].replace(REPLACE_TEXT_IMG,HEADER_TEXT))
		_file.writelines("\n")
	else:
		next_line_will_be_comment = 1
	if (TMP_HEADER == HEADER_TEXT):
		print(PRINT_COLOR["WARNING"] + "WARNING: 2 picture has same comment and attribute")
		print(f"\tPlz check line {CURR_LINE - 1}")
	TMP_HEADER = HEADER_TEXT

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

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print(PRINT_COLOR["ERROR"] + "ERROR: No primary key")
		exit()
	else:
		PRIMARY_KEY = " ".join(sys.argv[1:])
	with open("E:/Learning/00_Git/00_Learning/02_Python/02_Tools/01_Seo_Replacetext_YODY/IN.html", \
						"r", \
						encoding="utf8") \
	as f:
		input_file = f.readlines()

	# print(len(input_file))
	for _line in input_file:
		if("<img data-thumb" in _line):
			IMG_TXT_INFO.extend(_line.replace(img_txt_replace,img_txt_to).\
															split("><")[1:-1])
	# print(IMG_TXT_INFO)
	IMG_CMT_INFO=[picture_comment]*(len(IMG_TXT_INFO))
	# print(len(IMG_CMT_INFO))
	for index in range(len(IMG_TXT_INFO)):
		IMG_TXT_INFO[index] = IMG_TXT_INFO[index].\
										replace(img_txt_to[1:], img_txt_to)
		IMG_TXT_INFO[index] = IMG_TXT_INFO[index].\
										replace("\" /", "\" /></p>")
	write_idx = 0
	with open("E:/Learning/00_Git/00_Learning/02_Python/02_Tools/01_Seo_Replacetext_YODY/OUT.html", \
						"w", \
						encoding="utf8") \
	as out_file:
		for _line in input_file:
			get_header(_line)
			if img_txt_replace in _line:
				continue
			if replace_pattern in _line:
				if (HEADER == HEADER_DEFALT):
					print(PRINT_COLOR["ERROR"] + "ERROR: Picture without comment or attribute")
					print(f"\tPlz check line {CURR_LINE + 1}")
					# print(f"Plz check image number {write_idx + 1} "
					# 	+ f"(find: {HEADER}), "
					# 	+ f"update comment and attribute!!!!\n"
					# 	+ f"PLZ CHECK line {CURR_LINE + 1} in HTML format")
				if (write_idx > (len(IMG_TXT_INFO) - 1)):
					CURR_LINE += 1
					out_file.writelines(_line)
					print(PRINT_COLOR["ERROR"] + "ERROR: No more pictures to replace")
					print(f"\tPlz check line {CURR_LINE}")
					# print(f"There are too only {len(IMG_TXT_INFO)} pictures, "
					# 	+ f"but there are too many places to replace ({write_idx + 1} places)\n"
					# 	+ f"Skip at line {CURR_LINE}, PLZ CHECK THAT")
				else:
					write_img_back(out_file, write_idx)
					write_idx += 1
			else:
				CURR_LINE += 1
				if (next_line_will_be_comment == 1):
					_tmp = _line.replace("<p dir=\"ltr\">", text_align_center + "<em>")
					_tmp = _tmp.replace("</p>", "</em></p>")
					out_file.writelines(_tmp)
					next_line_will_be_comment = 0
				else:
					out_file.writelines(_line)
	print(sys.argv)