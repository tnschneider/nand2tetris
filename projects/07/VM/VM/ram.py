class RAM:
	def __init__(self, start, end):
		self._endAddress = end
		self._currentAddress = start

	def nextAddress(self):
		addr = self._currentAddress
		if addr is None:
			raise Exception('Out of memory')
		
		if self._currentAddress < self._endAddress:
			self._currentAddress += 1
		else:
			self._currentAddress = None

		return addr