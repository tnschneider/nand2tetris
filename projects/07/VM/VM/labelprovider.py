class LabelProvider:
	def __init__(self):
		self._seed = 1

	def getLabel(self):
		label = 'LABEL' + str(self._seed)
		self._seed += 1
		return label