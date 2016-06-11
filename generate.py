from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pdb

class FooterCanvas(canvas.Canvas):

	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self.pages = []

	def showPage(self):
		self.pages.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		page_count = len(self.pages)
		for page in self.pages:
			self.__dict__.update(page)
			self.draw_canvas(page_count)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_canvas(self, page_count):
		page = 'Page {0} of {1}'.format(self._pageNumber, page_count)
		x = 128
		self.saveState()
		pdfmetrics.registerFont(TTFont('OpenSans', '/usr/share/fonts/OpenSans-Regular.ttf'))
		self.setFont('OpenSans', 10)
		self.setStrokeColorRGB(0, 0, 0)
		self.setLineWidth(0.5)
		self.drawCentredString(120, letter[1] - 30, 'Network Device Report')
		self.drawString(letter[0] - 120, letter[1] - 30, page)	
		self.line(66, letter[1] - 40, letter[0] - 66, letter[1] - 40)
		self.line(66, 78, letter[0] - 66, 78)
		#self.drawCentredString(letter[0] / 2, 65, page)	
		self.drawImage('logo-blue.jpg', letter[0] - 175, 25, height=50, width=120)
		#self.drawString(letter[0]-x, 25, page)
		self.restoreState()


styles = getSampleStyleSheet()
elements = []
#elements.append(Image('logo-blue.png', height=103, 250))
#elements.append(Paragraph("Hello"))
#elements.append(Paragraph("World"))
elements.append(PageBreak())
elements.append(PageBreak())
elements.append(PageBreak())
#elements.append(Paragraph("You are in page 2"))

doc = SimpleDocTemplate("device_report.pdf", pagesize=letter)
doc.multiBuild(elements, canvasmaker=FooterCanvas)
