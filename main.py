from assignment5 import *

def main():
	nr = 0
	while nr != 7:
		str = "\n"
		for _ in range(0, 40):
			str += "-"
		print(str)
		print "type a number for board"
		print "1: easy"
		print "2: medium"
		print "3: hard"
		print "4: very hard"
		print "5: not so extreme"
		print "6: worlds hardest sudoku"
		print "7: quit"

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
		elif nr == 5:
			file = "files/extreme.txt"
		elif nr == 6:
			file = "files/isdisextreme.txt"
		else:
			continue

		csp = create_sudoku_csp(file)

		solution = csp.backtracking_search()
		if solution == "failure":
			print "failure"
		else:
			csp.backtrack_performance()
			print_sudoku_solution(solution)



# application entry point
if __name__ == '__main__':
    main()
