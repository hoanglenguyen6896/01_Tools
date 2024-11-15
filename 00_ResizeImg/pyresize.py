from PIL import Image # equal "import PIL.Image", you can't import PIL then invoke PIL.Image
import textwrap3
import piexif
import os
from unidecode import unidecode
import shutil
import argparse
from tkinter import messagebox

TARGET_WIDTH = 750

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

IN_IMG_DIR = SCRIPT_ABS_PATH + "/IN_DIR"
OUT_IMG_DIR = SCRIPT_ABS_PATH + "/OUT_DIR"
LOGO_PATH = SCRIPT_ABS_PATH + "/logo"
ERR = 0
class all_image_stuff:
    def __init__(self,
                 input_dir = IN_IMG_DIR,
                 output_dir = OUT_IMG_DIR,
                 author = None,
                 add_logo = None):
        global ERR
        ERR = 0
        self.author = author
        self.add_logo = add_logo
        self.logo_file = None
        if input_dir[-1] == "/":
            self.indir = input_dir
        else:
            self.indir = input_dir + "/"
        # Check if input directory exists
        if not (os.path.isdir(self.indir)):
            messagebox.showerror("Error", f"{self.indir} does not exist")
            ERR = 1
            return None
        if output_dir[-1] == "/":
            self.outdir = output_dir
        else:
            self.outdir = output_dir + "/"
        # Check if output directory exists then create it
        if not (os.path.isdir(self.outdir)):
            print("Creating output directory " + self.outdir)
            os.mkdir(self.outdir)
        elif len(os.listdir(self.outdir)) != 0:
            # If exists and not empty, empty output directory
            print("Empty", self.outdir)
            for _dir in os.listdir(self.outdir):
                # print(_dir)
                try:
                    shutil.rmtree(self.outdir + _dir)
                except NotADirectoryError as __tmp:
                    print("Skip", _dir, __tmp)
                except Exception as _tmp:
                    messagebox.showerror("Error", f"Something wrong when clean {self.outdir} - {_tmp}")
                    ERR = 1
                    return None
                    # print("Something wrong when clean", self.outdir, _tmp)
        self.all_dir = []
        # list all dir in input directory
        _tmp_all_dir = os.listdir(self.indir)
        for _obj in _tmp_all_dir:
            if (os.path.isdir(self.indir + _obj)):
                # Get subdir only then create corresponding output subdir
                self.all_dir.append(_obj)
                if not os.path.isdir(self.outdir + _obj):
                    os.mkdir(self.outdir + _obj)
                else:
                    messagebox.showerror("Error", "Output directory should be empty!!!")
                    ERR = 1
                    return None
                pass
            else:
                pass
        if len(self.all_dir) == 0:
            messagebox.showerror("Error", f"Input {self.indir} dir is empty!!!")
            ERR = 1
            return None
        pass

    def _convert_utf16_to_hex_exif(self, target_str):
        # Get utf-16 of string
        # Append ending to table_result fffeabcd > abcd
        table_word_16 = []
        for item in target_str:
            table_word_16.append(item.encode('utf-16').hex().replace('fffe',''))
        # Split into string size 2
        table_word_8 = []
        for word16 in table_word_16:
            table_word_8.append(word16[0:2])
            table_word_8.append(word16[2:])
        # Convert string size 2 to hex int
        table_result = []
        for word8 in table_word_8:
            table_result.append(int(word8, 16))
        return table_result


    # Add description (title, subject, rate, tags, comment) to image
    def _set_img_des_from_exif(self, _dir_name, _author, exifdata):
        # remove exif data if exist as some of them may contain can't parse info
        # print(exifdata)
        focus_key = self._convert_utf16_to_hex_exif(_dir_name)
        exifdata['Exif'] = {}
        exifdata['0th'][IMG_EXIF_DES["Title"]] = str.encode(_dir_name) # Set both title and subject
        exifdata['0th'][IMG_EXIF_DES["Rating"]] = 5  # Set rating
        exifdata['0th'][IMG_EXIF_DES["RatingPercent"]] = 99 # Set rating, need both
        focus_key.extend((0, 0))
        exifdata['0th'][IMG_EXIF_DES["Keywords"]] = tuple(focus_key) # Set tags
        exifdata['0th'][IMG_EXIF_DES["Comment"]] = tuple(focus_key) # Set comment
        # Set author
        if self.author != None:
            author = self._convert_utf16_to_hex_exif(_author)
            author.extend((0, 0))
            exifdata['0th'][IMG_EXIF_DES["Copyright"]] = str.encode(_author)
            exifdata['0th'][IMG_EXIF_DES["Author_str"]] = str.encode(_author)
            exifdata['0th'][IMG_EXIF_DES["Author_utf16"]] = tuple(author)
        # print(exifdata)
        # exit(-1)
        return exifdata

    # Resize a single image
    def resize_a_single_image(self, _dir_name, in_file, out_file, logo_image):
        # print(in_file, out_file)
        # print(imghdr.what(in_file))
        # return
        global ERR

        if out_file.endswith("jpg") != True:
            for img_type in ["jpg", "png", "webp", "jpeg", \
                                "bpm", "nef", "tif", "tiff"]:
                if out_file.endswith(img_type) == True:
                    out_file = out_file[:-len(img_type)] + "jpg"
                    break
        # print(out_file)
        # return
        with Image.open(in_file) as image:
            if image.mode != "RGB":
                rgb_img = image.convert("RGB")
            else:
                rgb_img = image.convert("RGB")
            # Enlarge
            if rgb_img.width < TARGET_WIDTH:
                _ratio = TARGET_WIDTH/rgb_img.width
                rgb_img = rgb_img.resize((TARGET_WIDTH,
                                        int(_ratio*rgb_img.height)),
                                        Image.Resampling.LANCZOS)
            # Reduce
            elif rgb_img.width > TARGET_WIDTH:
                rgb_img.thumbnail((TARGET_WIDTH, 9999))

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
                messagebox.showwarning("Warning", f"Something wrong with exif of {in_file}, it will be skipped")
                return
            exifdata['Interop'] = {}
            exifdata['1st'] = {}
            exifdata['thumbnail'] = None
            try:
                # Dunp human readable exif to image exif
                exif_bytes = piexif.dump(self._set_img_des_from_exif(
                                            _dir_name,
                                            self.author,
                                            exifdata))
                # print(exif_bytes)
                # Save image with dumped exif
                if logo_image != None:
                    rgb_img.paste(logo_image,
                                    (rgb_img.width - logo_image.width,
                                        rgb_img.height - logo_image.height),
                                    logo_image)
                rgb_img.save(out_file, exif=exif_bytes)
            except Exception as e:
                print(in_file, "Error", e)
                messagebox.showerror("Error", f"Can't convert image {in_file}")

    # Resize all images in a single directory
    def resize_all_image_in_a_dir(self, _dir_name,
                                input_full_path,
                                output_full_path,
                                logo_image):
        for _img in os.listdir(input_full_path):
            _in = input_full_path + "/" + _img
            _out = output_full_path + "/" \
                                + unidecode(
                                    _dir_name.replace(" ", "-").lower()) \
                                + "-" + _img.split(".")[0] + "." \
                                + _img.split(".")[1]
            self.resize_a_single_image(_dir_name,
                                    _in,
                                    _out,
                                    logo_image)

    def resize_target_logo(self):
        logo_file = None
        if self.add_logo != None:
            if os.path.isfile(self.add_logo):
                self.logo_file = self.add_logo
            else:
                logo_file_list = os.listdir(LOGO_PATH)
                for _img_file in logo_file_list:
                    if self.add_logo in _img_file:
                        self.logo_file = LOGO_PATH + "/" + _img_file
                        break
            if self.logo_file == None:
                print("Can't find logo of", self.add_logo)
            else:
                logo_file = Image.open(self.logo_file)
                if logo_file.mode != "RGBA":
                    rgb_img = logo_file.convert("RGBA")
                else:
                    rgb_img = logo_file
                # Enlarge
                if rgb_img.width < 150:
                    _ratio = 150/rgb_img.width
                    rgb_img = rgb_img.resize((150,
                                            int(_ratio*rgb_img.height)),
                                            Image.Resampling.LANCZOS)
                # Reduce
                elif rgb_img.width > 150:
                    rgb_img.thumbnail((150, 150))
                # rgb_img.putalpha(180)
        return logo_file

    # Resize all images in all subdirectories of input directory
    def resize_all_image_in_input_subdirs(self):
        if ERR == 1:
            return ERR
        logo_image = self.resize_target_logo()
        for _dir_name in self.all_dir:
            input_full_path = self.indir + _dir_name
            output_full_path = self.outdir + _dir_name
            self.resize_all_image_in_a_dir(_dir_name,
                                        input_full_path,
                                        output_full_path,
                                        logo_image)
        if logo_image != None:
            logo_image.close()
        return ERR

if __name__ == '__main__':
    def argparse_init():
        parser = argparse.ArgumentParser(
                    prog=__file__,
                    description='Resize all images in subdir of IN_DIR, output to OUT_DIR',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog=textwrap3.dedent('''
                        Guide:
                            If you doesn't provide input and output, it will be set to default value:
                                Input as IN_DIR
                                Output as OUT_DIR
                            With input and output part
                                python pyresize.py -a YODY.VN -i D:/work/INPUT -o D:/work/OUTPUT
                        '''))
        parser.add_argument('-i', '--input', default=IN_IMG_DIR,
                            help="Path to input directory where you save all origin images in subdirs")
        parser.add_argument('-o', '--output', default=OUT_IMG_DIR,
                            help="Path to output directory")
        parser.add_argument('-a', '--author', default=None,
                            help="Author to be set")
        parser.add_argument('--add-logo', choices=(None, 'yody'),
                            type=str.lower, default=None,
                            help="Add logo to image (yody)?")
        return parser.parse_args()

    argv = argparse_init()

    if argv.author == None:
        uin_put = input("Add author or not (Y/N)?\n>> ")
        if uin_put.lower() in ["y", "yes"]:
            argv.author = input("Add author to be use:\n>> ")

    if argv.add_logo == None:
        uin_put = input("Add logo or not (Y/N)?\n>> ")
        if uin_put.lower() in ["y", "yes"]:
            logo_file_list = os.listdir(LOGO_PATH)
            logo_list = [x.split(".")[0] for x in logo_file_list]
            argv.add_logo = input(f"Add logo to be use ({logo_list})\n>> ")

    confirm = "N"
    while True:
        print("Are these correct?")
        if argv.author == None:
            print("\tNo author and copyright to be set")
        else:
            print("\tAuthor and copyright will be set to:", argv.author)

        if argv.add_logo == None:
            print("\tNo logo to be set")
        else:
            print("\tLogo", argv.add_logo, "will be use")
        confirm = input("(Y/N)?\n>> ")
        if confirm.lower() in ["y", "yes"]:
            break
        uin_put = input("Add author or not (Y/N)?\n>> ")
        if uin_put.lower() in ["y", "yes"]:
            argv.author = input("Add author to be use:\n>> ")

        uin_put = input("Add logo or not (Y/N)?\n>> ")
        if uin_put.lower() in ["y", "yes"]:
            logo_file_list = os.listdir(LOGO_PATH)
            logo_list = [x.split(".")[0] for x in logo_file_list]
            argv.add_logo = input(f"Add logo to be use ({logo_list})\n>> ")

    tmp = all_image_stuff(
        argv.input,
        argv.output,
        argv.author,
        argv.add_logo
    )
    tmp.resize_all_image_in_input_subdirs()
