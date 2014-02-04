import time
from optparse import OptionParser

from sh import tail
from PIL import Image, ImageFont, ImageDraw

FOREGROUND = (255, 255, 255)
WIDTH = 1920
HEIGHT = 1080
FONT = '/usr/share/fonts/TTF/DroidSans.ttf'
FONT_SIZE = 14
LINE_HEIGHT = 20
REFRESH = 0
DEFAULT_IMAGE = 'out.png'

parser = OptionParser(usage="%prog -f PATH [options]")
parser.add_option("-f", "--file", dest="file_path",
                  help="path to file to read data from", metavar="PATH")
parser.add_option("-i", "--image", dest="image_path", default=DEFAULT_IMAGE,
                  help="path to image to write to", metavar="PATH")
parser.add_option("--width", default=WIDTH, dest="width", type="int",
                  help="width of image", metavar="INT")
parser.add_option("--height", default=HEIGHT, dest="height", type="int",
                  help="height of image", metavar="INT")
parser.add_option("--font", default=FONT, dest="font",
                  help="path to a .ttf", metavar="PATH")
parser.add_option("--font-size", default=FONT_SIZE, dest="font_size", type="int",
                  help="font size of text", metavar="INT")
parser.add_option("--line-height", default=LINE_HEIGHT, dest="line_height", type="int",
                  help="line height of text", metavar="INT")
parser.add_option("-r", "--refresh", default=REFRESH, dest="refresh", type="int",
                  help="time in seconds between reading the file, DEFAULT: 0 - no refresh", metavar="INT")
parser.add_option("--reverse", dest="reverse", action="store_true",
                  help="reverse output")

options, args = parser.parse_args()
if not options.file_path:
    parser.error('Path to file not given')

try:
    with open(options.file_path) as f:
        font = ImageFont.truetype( options.font
                                 , options.font_size
                                 , encoding='unic'
                                 )

        while True:
            bg = Image.new('RGBA', (options.width, options.height), "#000000")
            draw = ImageDraw.Draw(bg)
            h = 0
            time.sleep(options.refresh)
            for l in tail( "-n " + str(int(options.height / options.line_height))
                            , options.file_path
                            , _iter=True
                            ):
                l = l.decode('utf-8').rstrip()
                h += options.line_height
                if h > options.height:
                    break
                if options.reverse:
                    y = 0 + h - options.line_height
                else:
                    y = options.height - h
                draw.text((0, y), l, font = font, fill = FOREGROUND)
            bg.save(options.image_path)
            if options.refresh == 0:
                break
            del bg
            del draw

except IOError:
    print options.file_path + ' not found.'

