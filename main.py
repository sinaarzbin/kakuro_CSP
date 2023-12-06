import threading
import graphics
from kakuro import Kakuro
import csp
import boards
import time

board = boards.hard2

csp.DELAY = 0
filtering = csp.ARC_CONSISTENCY
variable_ordering = csp.MCV
value_ordering = csp.LCV

if __name__ == '__main__':
    kak = Kakuro(board, filtering=filtering, variable_ordering=variable_ordering, value_ordering=None)


    def csp_calc():
        start = time.time()
        result = csp.backtrack(kak)
        end = time.time()
        if result is None:
            print("No solution")
        print("Time: %.2f" % (end - start))


    csp_thread = threading.Thread(target=csp_calc)
    csp_thread.start()

    graphics.start_graphic(kak)
