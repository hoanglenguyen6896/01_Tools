#!/c/Python/Python311/python3
import os

# equal "import PIL.Image", you can't import PIL then invoke PIL.Image
from PIL import Image

import piexif
from unidecode import unidecode

from common import *

class ImageToolsWithPIL:
	def __init__(self,
			  input_dir=IN_IMG_DIR,
			  output_dir=OUT_IMG_DIR,
			  author_name="",
			  cfg_img_width=IMG_DEFAULT_WIDTH,
			  cfg_img_height=IMG_DEFAULT_HEIGHT,
			  logodata = (LogoData("", 150, None, ""), ),
			  action = RESIZE):
		global NO_ERR
		NO_ERR = True
		self.action = action
		self.input_dir=input_dir
		self.input_subdirs = []
		self.output_dir=output_dir
		self.cfg_img_width=cfg_img_width
		self.cfg_img_height=cfg_img_height
		self.author = author_name
		self.logodata = []
		# pr(type(logodata))
		for _logo in logodata:
			if type(_logo) is not LogoData:
				_logo = LogoData(None, None, None, None)
				show_err(f"Logo {_logo} is selected but not valid")
			# else:
			# 	if not os.path.isfile(_logo.path):
			# 		_logo = LogoData(None, None, None, None)
			# 		show_err(f"Logo {_logo} does not exist")
			# 	elif _logo.path.split(".")[-1].upper() not in "PNG JPG JPEG TIFF TIF BMP GIF WEBP NEF":
			# 		_logo = LogoData(None, None, None, None)
			# 		show_err(f"Logo {_logo} is not valid image PNG JPG JPEG TIFF TIF BMP GIF WEBP NEF")
			self.logodata.append(_logo)

		""" Create out if need """
		if (os.path.realpath(self.output_dir) == os.path.realpath(SCRIPT_ABS_PATH)):
			show_err("Output path cannot be set to script folder, please try again")
			return None
		else:
			NO_ERR = safe_remove(self.output_dir)

		if not NO_ERR:
			return None

		NO_ERR = safe_mkdir(self.output_dir)
		if not NO_ERR:
			return None

		if not os.path.isdir(self.input_dir):
			show_err("Input directory does not exist")
			return None

		""" Return err if there aren't any subdir in indir """
		self.input_subdirs = next(os.walk(self.input_dir))[1]
		if not self.input_subdirs:
			show_err("Input dir is empty")
			return None

		""" Create corresponding out subdir """
		for _obj in self.input_subdirs:
			if _obj in "__pycache__":
				continue
			NO_ERR = safe_mkdir(self.output_dir, _obj)
			if not NO_ERR:
				return None

	def resize_logo(self):
		# if os.path.isfile(self.logo_path):
		for logodata in self.logodata:
			# pr(vars(logodata))
			if (logodata.path is None) or (not os.path.isfile(logodata.path)):
				logodata.image_data = None
				pr(f"Skip logo {logodata.path}")
				continue
			else:
				pr(f"Using logo {logodata.path}")
			try:
				logodata.image_data = Image.open(logodata.path)
				logodata.image_data = logodata.image_data.convert("RGBA")
				# Enlarge
				if logodata.image_data.width < logodata.width:
					_ratio = logodata.width/logodata.image_data.width
					logodata.image_data = logodata.image_data.resize((logodata.width,
										int(_ratio*logodata.image_data.height)),
										Image.Resampling.LANCZOS)
				# Reduce
				elif logodata.image_data.width > logodata.width:
					logodata.image_data.thumbnail((logodata.width,
						logodata.width))
			except Exception as e:
				logodata.image_data = None
				show_err(f'Invalid logo file {e}')

	def _string_to_exif_data(self, target_str):
		# Get utf-16 of string
		# Append ending to table_result fffeabcd > abcd
		table_result = []
		for item in target_str:
			word16 = item.encode('utf-16').hex().replace('fffe','')
			table_result.append(int(word16[0:2], 16))
			table_result.append(int(word16[2:], 16))
		table_result.extend((0, 0))
		rs = tuple(table_result)
		# pr(rs)
		return rs

	# Add description (title, subject, rate, tags, comment) to image
	def _set_img_des(self, exifdata):
		# remove exif data if exist as some of them may contain can't parse info
		focus_key_exif = self._string_to_exif_data(self.sub_cwd)
		exifdata['Exif'] = {}
		# Set both title and subject
		exifdata['0th'][IMG_EXIF_DES["Title"]] = str.encode(self.sub_cwd)
		# Set rating
		exifdata['0th'][IMG_EXIF_DES["Rating"]] = 5
		# Set rating, need both
		exifdata['0th'][IMG_EXIF_DES["RatingPercent"]] = 99
		# Set tags
		exifdata['0th'][IMG_EXIF_DES["Keywords"]] = focus_key_exif
		# Set comment
		exifdata['0th'][IMG_EXIF_DES["Comment"]] = focus_key_exif
		# Set author
		if self.author is not None:
			# pr(self.author)
			exifdata['0th'][IMG_EXIF_DES["Copyright"]] = str.encode(self.author)
			exifdata['0th'][IMG_EXIF_DES["Author_str"]] \
				= str.encode(self.author)
			exifdata['0th'][IMG_EXIF_DES["Author_utf16"]] \
				= self._string_to_exif_data(self.author)
		# pr("....................", exifdata)
		return exifdata

	def _enlarge(self, image: Image.Image, w_or_h):
		img = None
		if w_or_h == 'w':
			_ratio = self.cfg_img_width/image.width
			img = image.resize((self.cfg_img_width,
									int(_ratio*image.height)),
									Image.Resampling.LANCZOS)
		else:
			_ratio = self.cfg_img_height/image.height
			img = image.resize((int(_ratio*image.width),
									self.cfg_img_height),
									Image.Resampling.LANCZOS)
		return img

	def _reduce(self, image: Image.Image, w_or_h = 'w'):
		if w_or_h == 'w':
			image.thumbnail((self.cfg_img_width, 9999))
		else:
			image.thumbnail((9999, self.cfg_img_height))

	def _crop(self, image: Image.Image, w_or_h):
		def _crop_tup(left, right, top, bottom):
			return (left, top, right, bottom)
		img = None
		if w_or_h == 'w':
			_left = int((image.width - self.cfg_img_width)/2)
			_right = int((image.width + self.cfg_img_width)/2)
			if (_right - _left) != self.cfg_img_width:
				_left = _right - self.cfg_img_width
			img = image.crop(_crop_tup(
				left=_left,
				right=_right,
				top=0,
				bottom=image.height
			))
		elif w_or_h == 'h':
			# Crop H
			_top = int((image.height - self.cfg_img_height)/2)
			_bot = int((image.height + self.cfg_img_height)/2)
			if (_bot - _top) != self.cfg_img_height:
				_bot = self.cfg_img_height - _top
			img = image.crop(_crop_tup(
				left=0,
				right=image.width,
				top=_top,
				bottom=_bot
			))
		else:
			_left = int((image.width - self.cfg_img_width)/2)
			_right = int((image.width + self.cfg_img_width)/2)
			if (_right - _left) != self.cfg_img_width:
				_left = _right - self.cfg_img_width
			_top = int((image.height - self.cfg_img_height)/2)
			_bot = int((image.height + self.cfg_img_height)/2)
			if (_bot - _top) != self.cfg_img_height:
				_bot = self.cfg_img_height - _top
			# pr(_left, _right, _top, _bot)
			img = image.crop(_crop_tup(
				left=_left,
				right=_right,
				top=_top,
				bottom=_bot
			))
		return img


	def resize_an_image(self, img_data: Image.Image, output_file_path: str):
		rgb_img = img_data.convert("RGB")
		if self.action == CROP:
			#  w = cfg_w
			EQUAL = 0
			BIG = 1
			LESS = 2

			_w_list = [rgb_img.width == self.cfg_img_width, rgb_img.width > self.cfg_img_width, rgb_img.width < self.cfg_img_width]
			_h_list = [rgb_img.height == self.cfg_img_height, rgb_img.height > self.cfg_img_height, rgb_img.height < self.cfg_img_height]
			"""
			w    h    Step 1    Step 2    Step 3    Step 4
			=    =    Skip
			=    >    Crop H
			=    <    Enlarge H Crop W
			>    =    Crop W
			>    >    w/h vs tw/th
								if > then Resize as h, crop w
								if < then Resize as w, crop h
								if = then Resize as w
			>    <    Enlarge H Crop W
			<    =    Enlarge W Crop H
			<    >    Enlarge W Crop H
			<    <    Enlarge W If H > then Crop H
								If H < then	Enlarge H	Crop W H
			"""
			if _w_list[EQUAL] and _h_list[EQUAL]:
				# pr("pass")
				pass
			elif (_w_list[EQUAL] and _h_list[BIG]) or (_w_list[BIG] and _h_list[EQUAL]):
				# pr("Crop wh")
				rgb_img = self._crop(image=rgb_img, w_or_h='wh')
			elif (_w_list[EQUAL] and _h_list[LESS]) or (_w_list[BIG] and _h_list[LESS]):
				# pr("Enlarge h, Crop wh")
				rgb_img = self._enlarge(image=rgb_img, w_or_h='h')
				rgb_img = self._crop(image=rgb_img, w_or_h='wh')
			elif (_w_list[LESS] and _h_list[EQUAL]) or (_w_list[LESS] and _h_list[BIG]):
				# pr("Enlarge w, Crop wh")
				rgb_img = self._enlarge(image=rgb_img, w_or_h='w')
				rgb_img = self._crop(image=rgb_img, w_or_h='wh')
			elif (_w_list[BIG] and _h_list[BIG]):
				_img_rat = rgb_img.width/rgb_img.height
				_target_rat = self.cfg_img_width/self.cfg_img_height
				# when w/h > tW/tH, after resize w > targetW, >> reduce as h then crop w
				if _img_rat > _target_rat:
					self._reduce(rgb_img, 'h')
					rgb_img = self._crop(image=rgb_img, w_or_h='w')
				# when w/h < tW/tH, after resize h > targeth, >> reduce as w then crop h
				elif _img_rat < _target_rat:
					self._reduce(rgb_img, 'w')
					rgb_img = self._crop(image=rgb_img, w_or_h='h')
				else: # incase w/h =tw/th
					self._reduce(rgb_img, 'w')
				pass
			else:
				# pr("Enlarge w, check enlarge h, Crop wh")
				rgb_img = self._enlarge(image=rgb_img, w_or_h='w')
				if rgb_img.height < self.cfg_img_height:
					rgb_img = self._enlarge(image=rgb_img, w_or_h='h')
				rgb_img = self._crop(image=rgb_img, w_or_h='wh')
		elif self.action == RESIZE:
			# Enlarge
			if rgb_img.width < self.cfg_img_width:
				rgb_img = self._enlarge(image=rgb_img, w_or_h='w')
			# Reduce
			elif rgb_img.width > self.cfg_img_width:
				# rgb_img.thumbnail((self.cfg_img_width, 9999))
				self._reduce(rgb_img, 'w')
		try:
			exifdata = piexif.load(rgb_img.info["exif"])
		except KeyError:
			exifdata = {
				'0th': {},
				'Exif': {},
				'GPS': {},
				'Interop': {},
				'1st': {},
				'thumbnail': None
			}
		except:
			pr(f"Something wrong with exif {output_file_path} > [SKIP]")
			return
		exifdata['Interop'] = {}
		exifdata['1st'] = {}
		exifdata['thumbnail'] = None
		try:
			# Dunp human readable exif to image exif
			exif_bytes = piexif.dump(self._set_img_des(exifdata))

			# Paste logos
			def _get_x_y_pos(data):
				# Logo process is not fail, data is LogoData(path, width, image_data, pos)
				# pos is 0-8 (0 is 0-0)
				# 0 1 2
				# 3 4 5
				# 6 7 8
				# 0-0        half-0        max-0
				# 0-half     half-half     max-half
				# 0-max      half-max      max-max
				logoPos = data.pos
				x_max = int(rgb_img.width - data.image_data.width)
				y_max = int(rgb_img.height - data.image_data.height)
				if logoPos == 0:
					return (0,				0)
				elif logoPos == 1:
					return(int(x_max/2),	0)
				elif logoPos == 2:
					return (x_max,			0)
				elif logoPos == 3:
					return (0,				int(y_max/2))
				elif logoPos == 4:
					return (int(x_max/2),	int(y_max/2))
				elif logoPos == 5:
					return (x_max,			int(y_max/2))
				elif logoPos == 6:
					return (0,				y_max)
				elif logoPos == 7:
					return (int(x_max/2),	y_max)
				elif logoPos == 8:
					return (x_max,			y_max)

			for _logo in self.logodata:
				if _logo.image_data is not None:
					rgb_img.paste(_logo.image_data,
							_get_x_y_pos(_logo),
							_logo.image_data)

			# Save image with dumped exif
			rgb_img.save(output_file_path, exif=exif_bytes)
		except Exception as e:
			pr(f"Can't convert image {output_file_path}", e)


	def resize_each_subdir(self):
		_file_err = []
		for _img in next(os.walk(self.sub_input_path))[2]:
			input_file_path = os.path.join(self.sub_input_path, _img)
			# pr(input_file_path)
			# continue
			# result = is_image(input_file_path)
			try:
				input_file_data = Image.open(input_file_path)
				if input_file_data.format \
						in "PNG JPG JPEG TIFF TIF BMP GIF WEBP NEF":
					output_file_path = os.path.join(self.sub_output_path,
								unidecode(self.sub_cwd.replace(" ", "-").lower()) \
								+ "-" + _img.split(".")[0] \
								+ ".jpg")
					self.resize_an_image(input_file_data, output_file_path)
			except Exception as e:
				_file_err.append(input_file_path)
				pr(e)
		return _file_err
		# if _file_err:
		# 	show_err(f"File that cannot be processed {_file_err}")

	def resize_all(self):
		_file_err = []
		self.resize_logo()
		# return
		for _dir in self.input_subdirs:
			self.sub_cwd = _dir
			self.sub_input_path = os.path.join(self.input_dir, _dir)
			self.sub_output_path = os.path.join(self.output_dir, _dir)
			_file_err.extend(self.resize_each_subdir())
		for _data in self.logodata:
			if _data.image_data is not None:
				_data.image_data.close()
		return _file_err
