class Board:
	def __init__(self):
		self.something = 0

	def loadBoard(self, path)

        self.filepath = path
        file = open("file/" + self.filepath, "r")
        fileContent = file.readlines()

        self.width = len(fileContent[0]) - 1 #TODO: better way than -1?
        self.height = len(fileContent)

        x = 0
        y = 0

        # loop each character and create the board
        while(y < self.height):
            while(x < self.width):
                

                x += 1
            x = 0;
            y += 1
