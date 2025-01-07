#!/c/Python/Python311/python3
import os

# equal "import PIL.Image", you can't import PIL then invoke PIL.Image
from PIL import Image

import piexif
from unidecode import unidecode

from common import *

class ImageWithPIL:
	def __init__(self,
			  input_dir=IN_IMG_DIR,
			  output_dir=OUT_IMG_DIR,
			  author_name="",
			  img_width=IMG_DEFAULT_WIDTH,
			  logodata = LogoData("", 150, None, ""),
			  logodata_2 = LogoData("", 150, None, "")):
		global NO_ERR
		NO_ERR = True
		self.input_dir=input_dir
		self.input_subdirs = []
		self.output_dir=output_dir
		self.img_width=img_width
		self.author = author_name
		if type(logodata) is not LogoData:
			logodata = LogoData(None, None, None, None)
			show_err("Logo 1 is selected but not valid")
		if type(logodata_2) is not LogoData:
			logodata_2 = LogoData(None, None, None, None)
			show_err("Logo 2 is selected but not valid")
		self.logodata = (logodata, logodata_2)

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
			pr(vars(logodata))
			if (logodata.path is None) or (not os.path.isfile(logodata.path)):
				logodata.image_data = None
				pr(f"Skip logo {logodata}")
				continue
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
				show_err(e)

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

	def resize_an_image(self, img_data: Image.Image, output_file_path: str):
		rgb_img = img_data.convert("RGB")
		# Enlarge
		if rgb_img.width < self.img_width:
			_ratio = self.img_width/rgb_img.width
			rgb_img = rgb_img.resize((self.img_width,
									int(_ratio*rgb_img.height)),
									Image.Resampling.LANCZOS)
		# Reduce
		elif rgb_img.width > self.img_width:
			rgb_img.thumbnail((self.img_width, 9999))

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

			# if self.logodata[0] != None:
			# 	# paste logo
			# 	rgb_img.paste(self.logodata[0].image_data,
			# 					_get_x_y_pos(self.logodata[0]),
			# 					self.logodata[0].image_data)
			# if self.logodata[1] != None:
			# 	# paste logo
			# 	rgb_img.paste(self.logodata[1].image_data,
			# 					_get_x_y_pos(self.logodata[1]),
			# 					self.logodata[1].image_data)

			# Save image with dumped exif
			rgb_img.save(output_file_path, exif=exif_bytes)
		except Exception as e:
			pr(f"Can't convert image {output_file_path}", e)


	def resize_each_subdir(self):
		_file_err = []
		for _img in next(os.walk(self.sub_input_path))[2]:
			input_file_path = os.path.join(self.sub_input_path, _img)
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
