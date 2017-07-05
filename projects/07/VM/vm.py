import sys
from VM.parser import Parser
from VM.codewriter import CodeWriter
from VM.labelprovider import LabelProvider

inPath = sys.argv[1]
outPath = inPath.replace(".vm", ".asm")

parser = Parser(inPath)
writer = CodeWriter(outPath)

while parser.hasMoreCommands():
	parser.advance()

	if parser.commandType() in [parser.C_PUSH, parser.C_POP]:
		writer.writePushPop(parser.command(), parser.arg1(), parser.arg2())

	if parser.commandType() == parser.C_ARITHMETIC:
		writer.writeArithmetic(parser.command())


writer.close()