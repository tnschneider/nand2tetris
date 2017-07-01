import sys
from assembler.parser import Parser
from assembler.code import Translator
from assembler.symboltable import SymbolTable
from assembler.ram import RAM

asmPath = sys.argv[1]
outPath=asmPath.replace(".asm", ".hack")

outfile = open(outPath, 'w')

parser = Parser(asmPath)
symbols = SymbolTable()
trans = Translator()

instructions = []

#first pass to preload symbol table
line_num = 0
while parser.hasMoreCommands():
	parser.advance()
	if parser.commandType() == parser.L_COMMAND:
		symbols.addEntry(parser.symbol(), line_num)
	elif parser.commandType() == parser.A_COMMAND or parser.commandType() == parser.C_COMMAND:
		line_num += 1

parser.reset()
ram = RAM(16, 16383)

while parser.hasMoreCommands():
	parser.advance()

	if parser.commandType() == parser.A_COMMAND:
		sym = parser.symbol()
		if sym[0].isdigit():
			addr = int(sym)
		elif symbols.contains(sym):
			addr = symbols.getAddress(sym)
		else:
			addr = ram.nextAddress()
			symbols.addEntry(sym, addr)

		inst = trans.formatAInst(addr)
		instructions.append(inst)

	if parser.commandType() == parser.C_COMMAND:
		inst = trans.formatCInst(parser.dest(), parser.comp(), parser.jump())
		instructions.append(inst)

for line in instructions:
	outfile.write(line + '\n')
outfile.close()