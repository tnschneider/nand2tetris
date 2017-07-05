from instructionbuilder import InstructionBuilder
from labelprovider import LabelProvider

class CodeWriter:
	def __init__(self, path):
		self._file = open(path, 'w')
		self._labelProvider = LabelProvider()
		self._currentSourceFileName = ''
		initInst = self._init()
		self._file.write(initInst)

	def Builder(self):
		return InstructionBuilder(self._labelProvider)

	def setFileName(self, fileName):
		self._currentSourceFileName = fileName

	def getStaticSymbol(self, index):
		sym = self._currentSourceFileName + '.' + str(index)
		return sym

	def writeArithmetic(self, command):
		if command in ['neg', 'not']:
			cmd = self._arithmeticUnary(command)
		elif command in ['add', 'sub', 'and', 'or']:
			cmd = self._arithmeticBinary(command)
		elif command in ['eq', 'lt', 'gt']:
			cmd = self._compare(command)
		else:
			raise Exception("Bad command")
		#print('writing ', cmd)
		self._file.write(cmd)

	def writePushPop(self, command, segment, index):
		ib = self.Builder()
		if command == 'push':
			if segment == 'constant':
				cmd = ib.PUSH_CONSTANT(index).result()
			elif segment == 'pointer':
				cmd = ib.PUSH_POINTER(index).result()
			elif segment == 'static':
				cmd = ib.PUSH_STATIC(self.getStaticSymbol(index)).result()
			elif segment == 'local':
				cmd = ib.PUSH_MEM('LCL', index).result()
			elif segment == 'argument':
				cmd = ib.PUSH_MEM('ARG', index).result()
			elif segment == 'this':
				cmd = ib.PUSH_MEM('THIS', index).result()
			elif segment == 'that':
				cmd = ib.PUSH_MEM('THAT', index).result()
			elif segment == 'temp':
				cmd = ib.PUSH_TEMP(index).result()
			else:
				raise Exception("Bad Instuction")
		elif command == 'pop':
			if segment == 'static':
				cmd = ib.POP_STATIC(self.getStaticSymbol(index)).result()
			elif segment == 'pointer':
				cmd = ib.POP_POINTER(index).result()
			elif segment == 'local':
				cmd = ib.POP_MEM('LCL', index).result()
			elif segment == 'argument':
				cmd = ib.POP_MEM('ARG', index).result()
			elif segment == 'this':
				cmd = ib.POP_MEM('THIS', index).result()
			elif segment == 'that':
				cmd = ib.POP_MEM('THAT', index).result()
			elif segment == 'temp':
				cmd = ib.POP_TEMP(index).result()
			else:
				raise Exception("Bad Instruction")
		else:
			raise Exception("Bad Instruction")
		#print('writing ', cmd)
		self._file.write(cmd)

	def _init(self):
		return self.Builder().SET_STACK_POINTER('256').result()

	def _arithmeticUnary(self, command):
		return (self.Builder().DECR_SP()
			.LOAD_S0_TO_D()
			.EXACT(command)
			.LOAD_D_TO_S0()
			.INCR_SP()
			.result())

	def _arithmeticBinary(self, command):
		return (self.Builder()
			.DECR_SP()
			.LOAD_S1_TO_D()
			.GET_S0_ADDR()
			.LOAD_M_TO_A()
			.EXACT(command)
			.DECR_SP()
			.GET_S0_ADDR()
			.LOAD_D_TO_M()
			.INCR_SP()
			.result())

	def _compare(self, command):
		outJumpTrue = {}
		outJumpFalse = {}
		return (self.Builder()
			.DECR_SP()
			.LOAD_S1_TO_D()
			.LOAD_S0_TO_A()
			.C_INST('D', 'D-A', None)
			.JUMP('D', command, outJumpTrue)
			.DECR_SP()
			.LOAD_CONST_TO_S0('0')
			.JUMP_EXACT('0', 'JMP', outJumpFalse)
			.L_INST(outJumpTrue["label"])
			.DECR_SP()
			.LOAD_CONST_TO_S0('-1')
			.L_INST(outJumpFalse["label"])
			.INCR_SP()
			.result())
	

	def close(self):
		self._file.close()