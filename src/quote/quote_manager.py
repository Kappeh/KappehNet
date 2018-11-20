import random

from src.quote.quote import Quote

class QuoteManager:

	def __init__(self, filepath):
		self.filepath = filepath
		self.quotes = []

		self.loaded = False

	def load(self):
		if (self.loaded):
			return

		for line in open(self.filepath, 'r', encoding='utf-8'):
			quote = line.replace('\n', '').split('@')
			if (len(quote) != 2):
				continue
			self.quotes.append(Quote(quote[0], quote[1]))
		
		self.numQuotes = len(self.quotes)
		self.loaded = True

	def pickRandomQuote(self):
		if (not self.loaded and self.numQuotes == 0):
			return None

		n = random.randint(0, self.numQuotes - 1)
		return self.quotes[n]
