import pyPdf
import sys
import StringIO
import Canvas

# make sure it doesn't access a random place
assert len(sys.argv) >= 2
filename = sys.argv[1]

txt = open(filename)
packet = StringIO.StringIO()
cv = Canvas.Canvas()
cv.create_text(0, 500, text = txt)
cv.pack()
packet.seek(0)
with open("./scanOutput", "wb") as openfile:
	openfile.write(packet.getValue())


