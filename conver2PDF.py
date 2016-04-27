import pyPdf
import sys
import StringIO
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# make sure it doesn't access a random place
assert len(sys.argv) >= 2
filename = sys.argv[1]

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
for line in txt:
	line = line.replace ('\n', '')
	string.append(line)


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



report_line = False


cv.setFont("serif", FONT_SIZE_CONTENT)
for line in string:
        # insert an extra line for each nmap scan
        print line == ""
        if line == "":
            y -= 2 * Y_OFFSET
            report_line = False
            continue

        # add in tab
        if report_line:
	    cv.drawString(X_OFFSET, y, "    " + line)
        else:
            cv.drawString(X_OFFSET, y, line)
            y -= Y_OFFSET

	y -= Y_OFFSET
        report_line = True
        # reset y coordinate when it reaches the end of a page
        if y <= FONT_SIZE_TITLE:
            cv.showPage()
            y = PAGE_HEIGHT - SIZE_NEWPAGE
            cv.setFont('serif', FONT_SIZE_CONTENT)

	
cv.save()
packet.seek(0)
with open("./scanOutput.pdf", "wb") as openfile:
	openfile.write(packet.getvalue())


