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
			  logo_path="",
			  logo_width=LOGO_DEFAULT_WIDTH,
			  logo_pos=(LOGO_RIGHT, LOGO_BOTTOM)):
		global NO_ERR
		NO_ERR = True
		self.input_dir=input_dir
		self.input_subdirs = []
		self.output_dir=output_dir
		self.img_width=img_width
		self.author = author_name
		self.logo_path = logo_path
		self.logo_width=logo_width
		self.logo_data=None
		self.logo_pos=logo_pos

		""" Create out if need """
		NO_ERR = safe_remove(self.output_dir)
		if not NO_ERR:
			return None
		NO_ERR = safe_mkdir(self.output_dir)
		if not NO_ERR:
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
		if (self.logo_path is None) or (not os.path.exists(self.logo_path)):
			self.logo_data = None
			pr("No logo will be added")
			return
		try:
			self.logo_data = Image.open(self.logo_path)
			self.logo_data = self.logo_data.convert("RGBA")
			# Enlarge
			if self.logo_data.width < self.logo_width:
				_ratio = self.logo_width/self.logo_data.width
				self.logo_data = self.logo_data.resize((self.logo_width,
									int(_ratio*self.logo_data.height)),
									Image.Resampling.LANCZOS)
			# Reduce
			elif self.logo_data.width > self.logo_width:
				self.logo_data.thumbnail((self.logo_width,
					self.logo_width))
		except Exception as e:
			self.logo_data = None
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

			if self.logo_data != None:
				# paste logo
				if self.logo_pos[1] == LOGO_LEFT:
					_x_pos = 0
				else:
					_x_pos = rgb_img.width - self.logo_data.width
				if self.logo_pos[0] == LOGO_TOP:
					_y_pos = 0
				else:
					_y_pos = rgb_img.height - self.logo_data.height
				rgb_img.paste(self.logo_data,
								(_x_pos, _y_pos),
								self.logo_data)
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
		for _dir in self.input_subdirs:
			self.sub_cwd = _dir
			self.sub_input_path = os.path.join(self.input_dir, _dir)
			self.sub_output_path = os.path.join(self.output_dir, _dir)
			_file_err.extend(self.resize_each_subdir())
		if self.logo_data is not None:
			self.logo_data.close()
		return _file_err
