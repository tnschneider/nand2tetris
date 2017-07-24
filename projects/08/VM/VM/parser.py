import re

class Parser:
	def __init__(self, path):
		self.C_ARITHMETIC = 'C_ARITHMETIC'
		self.C_PUSH = 'C_PUSH'
		self.C_POP = 'C_POP'
		self.C_LABEL = 'C_LABEL'
		self.C_GOTO = 'C_GOTO'
		self.C_IF = 'C_IF'
		self.C_FUNCTION = 'C_FUNCTION'
		self.C_RETURN = 'C_RETURN'
		self.C_CALL = 'C_CALL'

		self._CMD_DICT = {
			'push': self.C_PUSH,
			'pop': self.C_POP,
			'label': self.C_LABEL,
			'goto': self.C_GOTO,
			'if-goto': self.C_IF,
			'function': self.C_FUNCTION,
			'return': self.C_RETURN,
			'call': self.C_CALL,
			'add': self.C_ARITHMETIC,
			'sub': self.C_ARITHMETIC,
			'neg': self.C_ARITHMETIC,
			'eq': self.C_ARITHMETIC,
			'gt': self.C_ARITHMETIC,
			'lt': self.C_ARITHMETIC,
			'and': self.C_ARITHMETIC,
			'or': self.C_ARITHMETIC,
			'not': self.C_ARITHMETIC
		}

		self._lines = []
		self._current_line = 0

		file = open(path, 'r')
		lines = file.read().split('\n')
		for line in lines:
			line = line.replace('\r', '')
			stripped = self._strip_line(line)
			if len(stripped) > 0:
				self._lines.append(stripped)

		self.reset()

	def reset(self):
		self._current_line = 0
		if len(self._lines) > self._current_line:
			self._next_command = self._lines[self._current_line]
		else:
			self._next_command = None

	def hasMoreCommands(self):
		return self._next_command is not None

	def advance(self):
		if self._next_command is not None:
			self._current_command = self._next_command

			if len(self._lines) > self._current_line + 1:
				self._next_command = self._lines[self._current_line + 1]
			else:
				self._next_command = None
			self._current_line += 1

	def commandType(self):
		command = self._getArg(0)
			
		if command in self._CMD_DICT:
			return self._CMD_DICT[command]
		raise Exception("Invalid command")

	def command(self):
		return self._getArg(0)

	def arg1(self):
		return self._getArg(1)
			
	def arg2(self):
		return self._getArg(2)

	def _getArg(self, ind):
		cmd = self._current_command
		fields = cmd.split(' ')
		if len(fields) < ind + 1:
			return None
		return fields[ind]

	def _strip_line(self, line):
		stripped = re.sub('//.*$', '', line)
		return stripped.strip().replace('\r', '')