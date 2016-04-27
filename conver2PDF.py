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

FONT_SIZE_TITLE = 50
FONT_SIZE_CONTENT = 20
SIZE_NEWPAGE = 60

PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]

txt = open(filename)
packet = StringIO.StringIO()
cv = canvas.Canvas(packet)
depth = 0
string = list()
for line in txt:
	line = line.replace ('\n', '')
	string.append(line)

pdfmetrics.registerFont(TTFont('serif', 'LiberationSerif-Regular.ttf'))
cv.setFont('serif', FONT_SIZE_TITLE)
y = PAGE_HEIGHT - SIZE_NEWPAGE
cv.drawString(PAGE_WIDTH / 2, y, "scan report")
y -= FONT_SIZE_TITLE

cv.setFont("serif", FONT_SIZE_CONTENT)
for line in string:
	cv.drawString(20, y, line)
	y -= FONT_SIZE_CONTENT
        # reset y coordinate when it reaches the end of a page
        if y <= FONT_SIZE_TITLE:
            cv.showPage()
            y = PAGE_HEIGHT - SIZE_NEWPAGE
            cv.setFont('serif', FONT_SIZE_CONTENT)

	
cv.save()
packet.seek(0)
with open("./scanOutput.pdf", "wb") as openfile:
	openfile.write(packet.getvalue())


