import pygame
import math
from random import shuffle

# Define some colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)

unsorted = [x * 5 for x in range(1, 80)]
shuffle(unsorted)
global highlighted
global sorting_type
sorters = ["Gnome Sort", "Insertion Sort"]
pygame.init()
#  Comparisons - Array accesses
stats = [0, 0]

class Screen_text(object):

    def __init__(self, text, pos):
        self.font = pygame.font.SysFont("Calibri", 25, True, False)
        self.screen_text = self.font.render(text, True, WHITE)
        self.pos = pos

    def draw(self):
        screen.blit(self.screen_text, self.pos)

    def update(self, new_text):
        self.screen_text = self.font.render(new_text, True, WHITE)

sorter = Screen_text(f"Sorter: {sorters[0]}", (10, 10))
stats_text = Screen_text(f"Comparisons: {stats[0]}     Array Accesses: {stats[1]}", (300, 10))


def draw_list(array):
    offset = 10
    bar_width = 10
    gap = 5
    y_pos = 595
    for index, bar in enumerate(array):
        if index in highlighted:
            pygame.draw.rect(screen, RED, [offset, y_pos - bar, bar_width, bar])
        else:
            pygame.draw.rect(screen, WHITE, [offset, y_pos - bar, bar_width, bar])
        offset += bar_width + gap

size = (1200, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Sorting Visualized")

done = False
clock = pygame.time.Clock()

def update(highlights):
    global highlighted
    highlighted = highlights
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
    screen.fill(BLACK)
    draw_list(unsorted)

    sorter.update(f"Sorter: {sorting_type}")
    sorter.draw()
    stats_text.update(f"Comparisons: {stats[0]}     Array Accesses: {stats[1]}")
    stats_text.draw()

    pygame.display.flip()
    x = clock.tick(100)


def gnome_sort():
    i = 0
    while True:
        if update([i, i- 1]):
            return
        if i == len(unsorted):
            global sorting_type
            sorting_type = None
            return
        elif i == 0:
            i += 1
        elif unsorted[i - 1] > unsorted[i]:
            stats[0] += 1
            stats[1] += 2
            tmp = unsorted[i]
            stats[1] += 1
            unsorted[i] = unsorted[i - 1]
            stats[1] += 1
            unsorted[i - 1] = tmp
            i -= 1
        else:
            i+=1

def insertion_sort():
    global sorting_type
    for i in range(1,len(unsorted)):
        j = i
        temp = unsorted[j]
        stats[1] += 1
        while j > 0 and temp < unsorted[j-1]:
            stats[0] += 1
            update([j, i])
            unsorted[j] = unsorted[j-1]
            stats[1] += 2
            j=j-1
        unsorted[j] = temp
    sorting_type = None

def selection_sort():
    global sorting_type
    for i in range(0, len(unsorted)):
        small = i
        for j in range(i, len(unsorted)):
            update([i, j, small])
            if unsorted[j] < unsorted[small]:
                small = j
        unsorted[i], unsorted[small] = unsorted[small], unsorted[i]
    sorting_type = None

def bubble_sort():
    global sorting_type
    s_length = len(unsorted) - 1
    while s_length > 0:
        for j in range(0, s_length):
            update([j, j + 1])
            stats[0] += 1
            stats[1] += 2
            if unsorted[j] > unsorted[j + 1]:
                unsorted[j], unsorted[j + 1] = unsorted[j + 1], unsorted[j]
                stats[1] += 3
        s_length -=1
    sorting_type = None

def help_me():
    availible_commands = ["Bubble", "Gnome", "Insertion", "Selection"]
    print("Availible sorting algorithms:")
    for command in availible_commands:
        print(command)
    print("Enter one of the availible commands below to run that algorithm")

def set_alg(alg):
    global sorting_type
    global unsorted
    sorting_type = alg + " Sort"

def get_sorter():
    command = input(">>> ")
    if command != "help":
        set_alg(command)
    else:
        help_me()


sorting_type = None

while not update([]):
    get_sorter()
    if sorting_type == "Gnome Sort":
        gnome_sort()
    elif sorting_type == "Insertion Sort":
        insertion_sort()
    elif sorting_type == "Selection Sort":
        selection_sort()
    elif sorting_type == "Bubble Sort":
        bubble_sort()
