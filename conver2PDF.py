import pyPdf
import sys
import StringIO
from reportlab.pdfgen import canvas

# make sure it doesn't access a random place
assert len(sys.argv) >= 2
filename = sys.argv[1]

txt = open(filename)
packet = StringIO.StringIO()
cv = canvas.Canvas(packet)
depth = 0
string = list()
for line in txt:
	line = line.replace ('\n', '')
	string.append(line)

y = 800
cv.drawString(200, y, "scan report")
y -= 50
for line in string:
	cv.drawString(20, y, line)
	y -= 20
	
cv.save()
packet.seek(0)
with open("./scanOutput.pdf", "wb") as openfile:
	openfile.write(packet.getvalue())


