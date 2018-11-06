from assignment5 import *
import sys
import getopt

def main():
	nr = 0
	while nr < 1 or nr > 4:
		print "type a number for board"
		print "1: easy"
		print "2: medium"
		print "3: hard"
		print "4: very hard"
		nr = input()

	file = ""
	if nr == 1:
		file = "./files/easy.txt"
	elif nr == 2:
		file = "files/medium.txt"
	elif nr == 3:
		file = "files/hard.txt"
	elif nr == 4:
		file = "files/veryhard.txt"

	csp = create_sudoku_csp(file)
	#for var in csp.variables:
	#	print var
	#	print csp.constraints[var]
	#	print "\n"


# application entry point
if __name__ == '__main__':
    main()
