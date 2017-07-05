def to_bin(self, value, length):
		fmt = '{0:0'+str(length)+'b}'
		return fmt.format(value)