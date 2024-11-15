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
import re
import argparse
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

FIRST_FOCUS_KEY_LINK = 0


def write_img_back(_file, _idx):
	global TMP_HEADER
	global CURR_LINE
	global PRIMARY_KEY
	CURR_LINE += 1
	_file.writelines(text_align_center)
	# Replace alt
	# print(get_similarity_ratio(HEADER_TEXT, PRIMARY_KEY))
	if get_similarity_ratio(HEADER_TEXT, PRIMARY_KEY) < 0.5:
		_file.writelines(IMG_TXT_INFO[_idx].replace(REPLACE_TEXT_IMG, f"{HEADER_TEXT} - {PRIMARY_KEY}"))
	else:
		_file.writelines(IMG_TXT_INFO[_idx].replace(REPLACE_TEXT_IMG, HEADER_TEXT))
	_file.writelines("\n")
	CURR_LINE += 1
	# Replace comment
	_file.writelines(IMG_CMT_INFO[_idx].replace(REPLACE_TEXT_IMG,HEADER_TEXT))
	_file.writelines("\n")
	if (TMP_HEADER == HEADER_TEXT):
		print(PRINT_COLOR["WARNING"] + "WARNING: 2 picture has same comment and attribute")
		print(f"\tPlz check line {CURR_LINE - 1}")
	TMP_HEADER = HEADER_TEXT

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

def link_focus_key_on_line(_line, _key_in_line, link = None):
	global FIRST_FOCUS_KEY_LINK
	find_result = re.search(_key_in_line, _line, re.IGNORECASE)
	if find_result != None:
		FIRST_FOCUS_KEY_LINK = 1
		_start = find_result.start()
		_end = find_result.end()
		full_key_link_bold_color = f"<a href=\"{link}\"><span style=\"color:#3498db;\"><strong>{_line[_start:_end]}</strong></span></a>"
		if re.search(full_key_link_bold_color, _line, re.IGNORECASE):
			print("No need to link")
			return _line
		# print(_subline)
		if link == None:
			print("No link to put", link)
			return _line
		return _line[:_start] + full_key_link_bold_color + _line[_end:] # replace 1 occurrence
	else:
		return _line

def link_yody(_line, yody_txt):
	find_result = re.search(yody_txt, _line, re.IGNORECASE)
	print(find_result)
	if find_result != None:
		_start = find_result.start()
		_end = find_result.end()
		full_key_link_bold_color = f"<a href=\"http://yody.vn\"><span style=\"color:#3498db;\"><strong>{yody_txt}</strong></span></a>"
		if re.search(full_key_link_bold_color, _line, re.IGNORECASE):
			print("No need to link yody")
			return _line
		# print(_subline)
		return _line[:_start] + full_key_link_bold_color + _line[_end:] # replace 1 occurrence
	else:
		return _line

if __name__ == "__main__":
	def argparse_init():
		parser = argparse.ArgumentParser(
					prog=__file__,
					description='Replace Image',
					# formatter_class=argparse.RawDescriptionHelpFormatter,
					# epilog=textwrap3.dedent('''
					#     Guide:
					#         If you doesn't provide input and output, it will be set to default value:
					#             Input as IN_DIR
					#             Output as OUT_DIR
					#         With input and output part
					#             python pyresize.py -a YODY.VN -i D:/work/INPUT -o D:/work/OUTPUT
					#     ''')
					)
		parser.add_argument('-k', '--key', default=None, required=True,
		                    help="Focus key")
		parser.add_argument('-l', '--link', default=None, required=False,
		                    help="Link for focus key")
		# parser.add_argument('-a', '--author', default=None,
		#                     help="Author to be set")
		# parser.add_argument('--add-logo', choices=(None, 'yody'),
		#                     type=str.lower, default=None,
		#                     help="Add logo to image (Y/N)?")
		return parser.parse_args()

	argv = argparse_init()

	if argv.key == None:
		print(PRINT_COLOR["ERROR"] + "ERROR: No primary key")
		exit()
	else:
		PRIMARY_KEY = argv.key
	with open("IN.html", \
						"r", \
						encoding="utf8") \
	as f:
		input_file = f.readlines()

	for _line in input_file:
		if("<img data-thumb" in _line):
			IMG_TXT_INFO.extend(_line.replace(img_txt_replace,img_txt_to).\
															split("><")[1:-1])
	IMG_CMT_INFO=[picture_comment]*(len(IMG_TXT_INFO))
	for index in range(len(IMG_TXT_INFO)):
		IMG_TXT_INFO[index] = IMG_TXT_INFO[index].\
										replace(img_txt_to[1:], img_txt_to)
		IMG_TXT_INFO[index] = IMG_TXT_INFO[index].\
										replace("\" /", "\" /></p>")
	write_idx = 0
	yody_line = None
	yody_txt = None
	input_file_reserve = input_file.copy()
	input_file_reserve.reverse()
	with open("OUT.html", \
						"w", \
						encoding="utf8") \
	as out_file:
		# Get last line that contain YODY or YODY.VN
		for _line in input_file_reserve:
			# input_line_idx += 1
			# print(input_line_idx,"-------------")
			if (img_txt_replace in _line) or (replace_pattern in _line):
				continue
			if "YODY.VN" in _line:
				yody_txt = "YODY.VN"
				yody_line = _line
				break
			elif "YODY" in _line:
				yody_txt = "YODY"
				yody_line = _line
				break
		for _line in input_file:
			get_header(_line)
			# Remove all image in html
			if FIRST_FOCUS_KEY_LINK == 0:
				_line = link_focus_key_on_line(_line, PRIMARY_KEY, argv.link)
			if (img_txt_replace in _line):
				continue
			if replace_pattern in _line:
				if (HEADER == HEADER_DEFALT):
					print(PRINT_COLOR["ERROR"] + "ERROR: Picture without comment or attribute")
					print(f"\tPlz check line {CURR_LINE + 1}")
				if (write_idx > (len(IMG_TXT_INFO) - 1)):
					CURR_LINE += 1
					out_file.writelines(_line)
					print(PRINT_COLOR["ERROR"] + "ERROR: No more pictures to replace")
					print(f"\tPlz check line {CURR_LINE}")
				else:
					# Write image with format
					write_img_back(out_file, write_idx)
					write_idx += 1
			else:
				CURR_LINE += 1
				if _line == yody_line:
					out_file.writelines(link_yody(_line, yody_txt))
				else:
					out_file.writelines(_line)
		if len(IMG_TXT_INFO) > write_idx:
			print(PRINT_COLOR["ERROR"] + "ERROR: Not all images are used")
	print(argv.key, "\n", argv.link)