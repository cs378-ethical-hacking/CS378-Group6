import pyPdf
import sys
import re
import StringIO
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
# make sure it doesn't access a random place
assert len(sys.argv) >= 2
length = len(sys.argv)
filename = sys.argv[length - 1]

# some constants
FONT_SIZE_TITLE = 40
FONT_SIZE_CONTENT = 15
FONT_SIZE_CLAIMER = 15
SIZE_NEWPAGE = 60
X_OFFSET = 50
Y_OFFSET = FONT_SIZE_CONTENT * 1.5
PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]


# read in txt file
txt = open(filename)
packet = StringIO.StringIO()
cv = canvas.Canvas(packet)
depth = 0
string = list()
new_line = True
for line in txt:
    if new_line:
        line = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group()
        line = "IP address: " + line
        new_line = False
    elif line == '\n':
        new_line = True
    line = line.replace ('\n', '')
    string.append(line)


highLight_OS = False

for i in xrange(1, length - 1):
    if sys.argv[i] == "-o":
        highLight_OS = True

# set headers
cv.setTitle("scan report")
pdfmetrics.registerFont(TTFont('serif', 'LiberationSerif-Regular.ttf'))
cv.setFont('serif', FONT_SIZE_TITLE)
y = PAGE_HEIGHT - SIZE_NEWPAGE
title = "scan report"
cv.drawString(PAGE_WIDTH / 2 - pdfmetrics.stringWidth(title, 'serif', FONT_SIZE_TITLE) / 2, y, title)

# make disclaimer
y -= FONT_SIZE_CLAIMER * 2
cv.setFont('serif', FONT_SIZE_CLAIMER)
claimer = "( the file is generated from " + filename + " ) "
cv.drawString(PAGE_WIDTH / 2 - pdfmetrics.stringWidth(claimer, 'serif', FONT_SIZE_CLAIMER) / 2, y, claimer)
y -= Y_OFFSET
y -= SIZE_NEWPAGE



cv.setFont("serif", FONT_SIZE_CONTENT)
for line in string:
        OS_line = False
        if highLight_OS and "OS" in line:
            OS_line = True
            
        if OS_line:
            cv.setFillColorRGB(1, 1, 0)
            cv.setStrokeColorRGB(1, 1, 0)
            width = pdfmetrics.stringWidth(line, 'serif', FONT_SIZE_CONTENT)
            cv.rect(X_OFFSET, y - FONT_SIZE_CONTENT/ 2.1, width + 1, FONT_SIZE_CONTENT * 1.1, fill = 1)
        cv.setFillColorRGB(0, 0, 0)
            
        # add in tab
        cv.drawString(X_OFFSET, y, line)
        y -= Y_OFFSET
        # reset y coordinate when it reaches the end of a page
        if y <= FONT_SIZE_TITLE:
            cv.showPage()
            y = PAGE_HEIGHT - SIZE_NEWPAGE
            cv.setFont('serif', FONT_SIZE_CONTENT)

cv.save()
packet.seek(0)
with open("./scanOutput.pdf", "wb") as openfile:
    openfile.write(packet.getvalue())


