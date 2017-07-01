class SymbolTable:
	def __init__(self):
		self._symbols = {
			"SCREEN": 8194,
			"KBD": 13851
		}

		self._nextMemAddress = 0

	def resolve(self, symbol):
		if symbol in self._symbols:
			return self._symbols[symbol]

		addr = self._nextMemAddress
		self._symbols[symbol] = addr
		self._nextMemAddress += 1
		return addr

	def setInstLabel(self, label, addr):
		self._symbols[label] = addr