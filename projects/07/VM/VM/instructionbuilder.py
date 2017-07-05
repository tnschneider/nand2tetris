_COPY_REGISTER = 15
def _TEMP_REGISTER(index):
	index = int(index)
	if index > 7 or index < 0:
		raise Exception('Temp register index out of range')
	return 'R' + str(5+index)

class InstructionBuilder:
	def __init__(self, labelProvider):
		self._ARITHM_DICT = {
			'add': 'D=D+A',
			'sub': 'D=D-A',
			'neg': 'D=-D',
			'eq': 'JEQ',
			'gt': 'JGT',
			'lt': 'JLT',
			'and': 'D=D&A',
			'or': 'D=D|A',
			'not': 'D=!D'
		}
		self._inst = ''
		self._labelNum = 0
		self._labelProvider = labelProvider

	def result(self):
		return self._inst

	def _pushInst(self, inst):
		if inst[-1] != '\n':
			inst = inst + '\n'
		self._inst += inst
		return self

	def _getLabel(self):
		return self._labelProvider.getLabel()

	def GET_S0_ADDR(self):
		return self._pushInst("@SP\nA=M\n")
	def GET_S1_ADDR(self):
		return self._pushInst("@SP\nA=M-1")
	def LOAD_S0_TO_D(self):
		return self._pushInst("@SP\nA=M\nD=M")
	def LOAD_D_TO_S0(self):
		return self._pushInst("@SP\nA=M\nM=D")
	def LOAD_S1_TO_D(self):
		return self._pushInst("@SP\nA=M-1\nD=M")
	def LOAD_D_TO_S1(self):
		return self._pushInst("@SP\nA=M-1\nM=D")
	def LOAD_S0_TO_A(self):
		return self._pushInst("@SP\nA=M\nA=M")
	def LOAD_S1_TO_A(self):
		return self._pushInst("@SP\nA=M-1\nA=M")
	def LOAD_D_TO_A(self):
		return self._pushInst("A=D")
	def LOAD_A_TO_D(self):
		return self._pushInst("D=A")
	def LOAD_M_TO_D(self):
		return self._pushInst("D=M")
	def LOAD_D_TO_M(self):
		return self._pushInst("M=D")
	def LOAD_M_TO_A(self):
		return self._pushInst("A=M")
	def INCR_SP(self):
		return self._pushInst("@SP\nM=M+1")
	def DECR_SP(self):
		return self._pushInst("@SP\nM=M-1")

	def A_INST(self, symbol):
		return self._pushInst('@' + str(symbol))
	def C_INST(self, dest, comp, jump):
		inst = ''
		if dest is not None:
			inst = dest + '='
		inst += comp
		if jump is not None:
			inst += ';' + jump
		return self._pushInst(inst)
	def L_INST(self, symbol):
		return self._pushInst('(' + symbol + ')')

	def SET_STACK_POINTER(self, addr):
		return (self.A_INST(addr)
			.LOAD_A_TO_D()
			.A_INST("SP")
			.LOAD_D_TO_M())
	def LOAD_CONST_TO_S0(self, const):
		if int(const) < 0:
			c = str(-(int(const)))
			return (self.A_INST(c)
				.LOAD_A_TO_D()
				.C_INST('D', '-D', None)
				.LOAD_D_TO_S0())
		else:
			return (self.A_INST(const)
				.LOAD_A_TO_D()
				.LOAD_D_TO_S0())


	def EXACT(self, command):
		cmd = self._ARITHM_DICT[command]
		return self._pushInst(cmd)
	def JUMP(self, comp, command, outLabel):
		cmd = self._ARITHM_DICT[command]
		return self.JUMP_EXACT(comp, cmd, outLabel)
	def JUMP_EXACT(self, comp, jump, outLabel):
		label = self._getLabel()
		outLabel["label"] = label
		return (self.A_INST(label)
			.C_INST(None, comp, jump))
		return inst 


#PUSH/POP
	def PUSH_CONSTANT(self, const):
		return self.LOAD_CONST_TO_S0(const).INCR_SP()
	def PUSH_MEM(self, segment, index):
		return (self.A_INST(index)
			.LOAD_A_TO_D()
			.A_INST(segment)
			.LOAD_M_TO_A()
			.C_INST('A', 'D+A', None)
			.LOAD_M_TO_D()
			.LOAD_D_TO_S0()
			.INCR_SP())
	def POP_MEM(self, segment, index):
		return (self.DECR_SP()
			.A_INST(index)
			.LOAD_A_TO_D()
			.A_INST(segment)
			.LOAD_M_TO_A()
			.C_INST('D', 'D+A', None)
			.A_INST(_COPY_REGISTER)
			.LOAD_D_TO_M()
			.LOAD_S0_TO_D()
			.A_INST(_COPY_REGISTER)
			.LOAD_M_TO_A()
			.LOAD_D_TO_M())
	def PUSH_POINTER(self, index):
		if index == '0':
			seg = 'THIS'
		elif index == '1':
			seg = 'THAT'
		else:
			raise Exception('Invalid pointer segment')
		return (self.A_INST(seg)
			.LOAD_M_TO_D()
			.LOAD_D_TO_S0()
			.INCR_SP())
	def POP_POINTER(self, index):
		if index == '0':
			seg = 'THIS'
		elif index == '1':
			seg = 'THAT'
		else:
			raise Exception('Invalid pointer segment')
		return (self.DECR_SP()
			.LOAD_S0_TO_D()
			.A_INST(seg)
			.LOAD_D_TO_M())
	def PUSH_TEMP(self, index):
		return (self.A_INST(_TEMP_REGISTER(index))
			.LOAD_M_TO_D()
			.LOAD_D_TO_S0()
			.INCR_SP())
	def POP_TEMP(self, index):
		return (self.DECR_SP()
			.LOAD_S0_TO_D()
			.A_INST(_TEMP_REGISTER(index))
			.LOAD_D_TO_M())
	def PUSH_STATIC(self, symbol):
		return (self.A_INST(symbol)
			.LOAD_M_TO_D()
			.LOAD_D_TO_S0()
			.INCR_SP())
	def POP_STATIC(self, symbol):
		return (self.DECR_SP()
			.LOAD_S0_TO_D()
			.A_INST(symbol)
			.LOAD_D_TO_M())

