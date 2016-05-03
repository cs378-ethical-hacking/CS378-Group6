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


class createPDF():
    def __init__(self):
        assert len(sys.argv) >= 2
        self.length = len(sys.argv)
        self.filename = sys.argv[self.length - 1]
        # some constants
        self.FONT_SIZE_TITLE = 40
        self.FONT_SIZE_CONTENT = 15
        self.FONT_SIZE_CLAIMER = 15
        self.SIZE_NEWPAGE = 60
        self.X_OFFSET = 50
        self.Y_OFFSET = self.FONT_SIZE_CONTENT * 1.5
        self.PAGE_WIDTH = defaultPageSize[0]
        self.PAGE_HEIGHT = defaultPageSize[1]
        self.packet = StringIO.StringIO()
        self.cv = canvas.Canvas(self.packet)
        self.highLightOS = False
        self.string = list()
    
    def input(self):
        # read in txt file
        txt = open(self.filename)
        depth = 0
        newLine = True
        for line in txt:
            line = line.strip()
            ss = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            if ss :
                line = "IP address: " + ss.group()
                
            line = line.replace ('\n', '')
            self.string.append(line)
        # user options
        for i in xrange(1, self.length - 1):
            if sys.argv[i] == "-o":
                self.highLightOS = True
        
    def createPDFFile(self):
        # set headers
        self.cv.setTitle("scan report")
        pdfmetrics.registerFont(TTFont('serif', 'LiberationSerif-Regular.ttf'))
        self.cv.setFont('serif', self.FONT_SIZE_TITLE)
        y = self.PAGE_HEIGHT - self.SIZE_NEWPAGE
        title = "scan report"
        self.cv.drawString(self.PAGE_WIDTH / 2 - pdfmetrics.stringWidth(title, 'serif', self.FONT_SIZE_TITLE) / 2, y, title)

        # make disclaimer
        y -= self.FONT_SIZE_CLAIMER * 2
        self.cv.setFont('serif', self.FONT_SIZE_CLAIMER)
        claimer = "( the file is generated from " + self.filename + " ) "
        self.cv.drawString(self.PAGE_WIDTH / 2 - pdfmetrics.stringWidth(claimer, 'serif', self.FONT_SIZE_CLAIMER) / 2, y, claimer)
        y -= self.Y_OFFSET
        y -= self.SIZE_NEWPAGE



        self.cv.setFont("serif", self.FONT_SIZE_CONTENT)
        for line in self.string:
            OSLine = False
            if self.highLightOS and "OS" in line:
                OSLine = True
            
            if OSLine:
                self.cv.setFillColorRGB(1, 1, 0)
                self.cv.setStrokeColorRGB(1, 1, 0)
                width = pdfmetrics.stringWidth(line, 'serif', self.FONT_SIZE_CONTENT)
                self.cv.rect(self.X_OFFSET, y - self.FONT_SIZE_CONTENT/ 2.1, width + 1, self.FONT_SIZE_CONTENT * 1.1, fill = 1)
            self.cv.setFillColorRGB(0, 0, 0)
            
            # add in tab
            self.cv.drawString(self.X_OFFSET, y, line)
            y -= self.Y_OFFSET
            # reset y coordinate when it reaches the end of a page
            if y <= self.FONT_SIZE_TITLE:
                self.cv.showPage()
                y = self.PAGE_HEIGHT - self.SIZE_NEWPAGE
                self.cv.setFont('serif', self.FONT_SIZE_CONTENT)

        self.cv.save()
        self.packet.seek(0)
        with open("./scanOutput.pdf", "wb") as openfile:
            openfile.write(self.packet.getvalue())



def main():
    c = createPDF()
    c.input()
    c.createPDFFile()


if __name__ == "__main__":
    main()
