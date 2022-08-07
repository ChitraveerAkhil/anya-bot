from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random

from fileOperations import FileOperations

# picture setup - it is set up for Twitter recommendations
WIDTH = 1024
HEIGHT = 512

# the margin are set by my preferences
MARGIN = 50
MARGIN_TOP = 50
MARGIN_BOTTOM = 150
LOGO_MARGIN = 25

# font variables
FONT_SIZES = [110, 100, 90, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20]
FONT_QUOTE = 'font-text'
FONT_QUOTED_BY = 'font-quoted-by'
FONT_SIZE = 'font-size'
FONT_QUOTED_BY_SIZE = 'font-quoted-by-size'

# Font colors
WHITE = 'rgb(255, 255, 255)'
GREY = 'rgb(200, 200, 200)'

# output text
OUTPUT_QUOTE = 'quote'
OUTPUT_QUOTED_BY = 'quoted-by'
OUTPUT_LINES = 'lines'


class QuoteMaker:

    def text_wrap_and_font_size(self, output, font_style, max_width, max_height):
        for font_size in FONT_SIZES:
            output[OUTPUT_LINES] = []
            font = ImageFont.truetype(
                font_style[FONT_QUOTE], size=font_size, encoding="unic")
            output[OUTPUT_QUOTE] = " ".join(output[OUTPUT_QUOTE].split())
            if font.getsize(output[OUTPUT_QUOTE])[0] <= max_width:
                output[OUTPUT_LINES].append(output[OUTPUT_QUOTE])
            else:
                words = output[OUTPUT_QUOTE].split()
                line = ""
                for word in words:
                    if font.getsize(line + " " + word)[0] <= max_width:
                        line += " " + word
                    else:
                        output[OUTPUT_LINES].append(line)
                        line = word
                output[OUTPUT_LINES].append(line)
            line_height = font.getsize('lp')[1]
            quoted_by_font_size = font_size
            quoted_by_font = ImageFont.truetype(
                font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic")
            while quoted_by_font.getsize(output[OUTPUT_QUOTED_BY])[0] > max_width//2:
                quoted_by_font_size -= 1
                quoted_by_font = ImageFont.truetype(
                    font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic")
            if line_height*len(output[OUTPUT_LINES]) + quoted_by_font.getsize('lp')[1] < max_height:
                font_style[FONT_SIZE] = font_size
                font_style[FONT_QUOTED_BY_SIZE] = quoted_by_font_size
                return True
        # we didn't succeed find a font size that would match within the block of text
        return False

    def draw_text(self, image, output, font_style):
        draw = ImageDraw.Draw(image)
        lines = output[OUTPUT_LINES]
        font = ImageFont.truetype(
            font_style[FONT_QUOTE], size=font_style[FONT_SIZE], encoding="unic")
        line_height = font.getsize('lp')[1]
        y = MARGIN_TOP
        for line in lines:
            x = (WIDTH - font.getsize(line)[0]) // 2
            draw.text((x, y), line, fill=WHITE, font=font)
            y = y + line_height
        quoted_by = output[OUTPUT_QUOTED_BY]
        quoted_by_font = ImageFont.truetype(
            font_style[FONT_QUOTED_BY], size=font_style[FONT_QUOTED_BY_SIZE], encoding="unic")
        # position the quoted_by in the far right, but within margin
        x = WIDTH - quoted_by_font.getsize(quoted_by)[0] - MARGIN
        draw.text((x, y), quoted_by, fill=GREY, font=quoted_by_font)
        return image

    def generate_image_with_quote(self, quote, quote_by, name):

        imgName = str(random.randint(0, 19))+".jpg"
        input_image = FileOperations.parseFileName('images', imgName)
        output_image = name
        #font_style = {FONT_QUOTE: "fonts/DynaPuff/DynaPuff_Condensed-Bold.ttf", FONT_QUOTED_BY: "fonts/DynaPuff/DynaPuff-Bold.ttf"}
        fontQuote = self.formFontType()
        fontQuotedBy = self.formFontType()
        font_style = {FONT_QUOTE: fontQuote, FONT_QUOTED_BY: fontQuotedBy}

        image = Image.open(input_image)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.5)
        image = image.resize((WIDTH, HEIGHT))
        output = {OUTPUT_QUOTE: quote, OUTPUT_QUOTED_BY: quote_by}
        self.text_wrap_and_font_size(output, font_style, WIDTH -
                                     2*MARGIN, HEIGHT - MARGIN_TOP - MARGIN_BOTTOM)
        image = self.draw_text(image, output, font_style)
        image.save(output_image)

    def formFontType(self):
        dir_list = FileOperations.getDirs('fonts')
        dirLn = len(dir_list)
        dirRanInt = random.randint(0, dirLn-1)
        drctry = dir_list[dirRanInt]
        files = FileOperations.getFiles(drctry, 'ttf')
        fileLn = len(files)
        fileRandInt = random.randint(0, fileLn-1)
        file = FileOperations.parseFileName(drctry, files[fileRandInt])
        return file


def main():
    quoteMaker = QuoteMaker()
    quoteMaker.generate_image_with_quote(
        'Test Quote', 'Test Quote Author', 'TestFile')


if __name__ == "__main__":
    main()
