
class Quote:

	def __init__(self, text, origin):
		self.text = text
		self.origin = origin

	def __str__(self):
		return self.text + " : " + self.origin
