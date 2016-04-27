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
cv.setFont('serif', 30)
y = PAGE_HEIGHT - 50
cv.drawString(PAGE_WIDTH / 2, y, "scan report")
y -= 50

cv.setFont("serif", 20)
for line in string:
	cv.drawString(20, y, line)
	y -= 20
	
cv.save()
packet.seek(0)
with open("./scanOutput.pdf", "wb") as openfile:
	openfile.write(packet.getvalue())


