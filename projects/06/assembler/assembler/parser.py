import re

class Parser:
	def __init__(self, path):
		self.L_COMMAND = "L_COMMAND"
		self.A_COMMAND = "A_COMMAND"
		self.C_COMMAND = "C_COMMAND"
		
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

	def hasMoreCommands(self):
		return self._next_command is not None

	def debugCmd(self):
		return self._current_command

	def reset(self):
		self._current_line = 0
		if len(self._lines) > self._current_line:
			self._next_command = self._lines[self._current_line]
		else:
			self._next_command = None

	def advance(self):
		if self._next_command is not None:
			self._current_command = self._next_command

			if len(self._lines) > self._current_line + 1:
				self._next_command = self._lines[self._current_line + 1]
			else:
				self._next_command = None
			self._current_line += 1

	def commandType(self):
		if self._current_command[0] == '(':
			return self.L_COMMAND
		if self._current_command[0] == '@':
			return self.A_COMMAND
		return self.C_COMMAND

	def symbol(self):
		return self._current_command.replace('(', '').replace(')', '').replace('@', '')

	def dest(self):
		cmd = self._current_command
		if '=' in cmd:
			return cmd.split('=')[0]
		return None

	def comp(self):
		cmd = self._current_command
		if '=' in cmd:
			cmd = cmd.split('=')[1]
		
		if ';' in cmd:
			cmd = cmd.split(';')[0]
		
		return cmd

	def jump(self):
		cmd = self._current_command
		if ';' in cmd:
			return cmd.split(';')[1]
		return None


	def _strip_line(self, line):
		stripped = re.sub('//.*$', '', line)
		return stripped.strip().replace('\r', '')