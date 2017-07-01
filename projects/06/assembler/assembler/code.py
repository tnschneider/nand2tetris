class Translator:
	def __init__(self):
		self._DEST_DICT = {
			'M': '001',
			'D': '010',
			'MD': '011',
			'A': '100',
			'AM': '101',
			'AD': '110',
			'AMD': '111'
		}

		self._JUMP_DICT = {
			'JGT': '001',
			'JEQ': '010',
			'JGE': '011',
			'JLT': '100',
			'JNE': '101',
			'JLE': '110',
			'JMP': '111'
		}

		self._COMP_A0_DICT = {
			'0': '101010',
			'1': '111111',
			'-1': '111010',
			'D': '001100',
			'A': '110000',
			'!D': '001101',
			'!A': '110001',
			'-D': '001111',
			'-A': '110011',
			'D+1': '011111',
			'A+1': '110111',
			'D-1': '001110',
			'A-1': '110010',
			'D+A': '000010',
			'D-A': '010011',
			'A-D': '000111',
			'D&A': '000000',
			'D|A': '010101'
		}

		self._COMP_A1_DICT = {
			'M': '110000',
			'!M': '110001',
			'-M': '110011',
			'M+1': '110111',
			'M-1': '110010',
			'D+M': '000010',
			'D-M': '010011',
			'M-D': '000111',
			'D&M': '000000',
			'D|M': '010101'	
		}

	def _dest(self, value):
		return self._DEST_DICT.get(value, '000')

	def _comp(self, value):
		value = value.replace('\r', '')
		isA1 = 'M' in value
		if isA1:
			return '1' + self._COMP_A1_DICT.get(value, '000000')
		return '0' + self._COMP_A0_DICT.get(value, '000000')

	def _jump(self, value):
		return self._JUMP_DICT.get(value, '000')

	def formatAInst(self, value):
		return self._to_bin(value, 16)

	def formatCInst(self, dest, comp, jump):
		return '111' + self._comp(comp) + self._dest(dest) + self._jump(jump)

	def _to_bin(self, value, length):
		fmt = '{0:0'+str(length)+'b}'
		return fmt.format(value)