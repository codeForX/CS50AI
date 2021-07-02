import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # completed by me 
        if self.count == len(self.count):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # completed by me
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # completed by me
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # completed by me
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        # completed by me
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # completed by me
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def nearbyCells(self,cell):
        """
        Returns cells that are neighbors with a given cell 
        while also ignoring any cells out of boundrys of the game.
        """
        # made by me
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if  (i,j) == cell :
                    continue
                elif (i,j) in self.moves_made:
                    continue
                elif  i < 0 or j < 0 or i >= self.height or j >= self.width:
                    continue
                cells.add((i,j))
        return cells


    def updateKnowledgePool(self):
        """
        updates the knowledge base based on things
        that could be infered from current knowledge
        """
        # made by me

        def purgeTheEmpty():
            """
            gets rid of empty sentences from which nothing could be infered
            to speed up the decisions
            """
            
            knowledgeCopy = self.knowledge.copy()
            for sentence in knowledgeCopy:
                if sentence.cells == set():
                    self.knowledge.remove(sentence)


        def inferNewKnowledge(sentance1, sentance2):
            """
            Given two sentemces it infers a third and cuts out the other two
            as thay are no longer needed.
            (for some reason the sentences dissapear from the knowledge sometimes
            but it dosent seem to affect program results.)
            """
            if sentance1 in  self.knowledge:
                self.knowledge.remove(sentance1)
            if sentance2 in  self.knowledge:
                self.knowledge.remove(sentance2)
            self.knowledge.append(Sentence(sentance1.cells - sentance2.cells, sentance1.count - sentance2.count))
        
        # remove already made moves.
        for sentence in self.knowledge:
            for move in self.moves_made:
                if move in sentence.cells:
                    sentence.cells.remove(move)

        purgeTheEmpty()

        knowledgeCopy = self.knowledge.copy()
        for sentance1 in knowledgeCopy:
            for sentance2 in knowledgeCopy:
                if sentance1 != sentance2 :
                    if  sentance2.cells.issubset(sentance1.cells) : 
                        inferNewKnowledge(sentance1, sentance2)
    
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # completed by me
        self.moves_made.add(cell)

        self.safes.add(cell)

        cells = self.nearbyCells(cell)
        self.knowledge.append(Sentence(cells,count))
        print(self.knowledge[-1])

        knowledgeCopy = self.knowledge.copy()
        for sentence in knowledgeCopy:
            if len(sentence.cells) == sentence.count:
                for spot in sentence.cells.copy():
                    self.mark_mine(spot)
            elif sentence.count == 0:
                for spot in sentence.cells.copy():
                    self.mark_safe(spot)

        self.updateKnowledgePool()
        print(len(self.knowledge))


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # completed by me
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # completed by me
        availableMoves = []
        for i in range(self.height):
            for j in range(self.width):
                availableMoves.append((i,j))
        move = random.choice([move for move in availableMoves if move not in self.moves_made and move not in self.mines])
        print(f"going to {move} wish me luck🤞")
        return move
