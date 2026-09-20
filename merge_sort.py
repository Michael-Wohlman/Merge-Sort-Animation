from manim import *

""" Variables to change (default is ARR = [38, 27, 43, 3, 9, 82, 10])"""
ARR = [38, 27, 43, 9, 82, 10]


""" Initializing the Output array with empty rows. """
# calculating how many rows needed for output
how_many_rows = 0
if len(ARR) == 2:
    how_many_rows = 3
elif len(ARR) < 5:
    how_many_rows = 5
elif len(ARR) < 9:
    how_many_rows = 7
elif len(ARR) <= 16:
    how_many_rows = 9

"""
# first row is original array
output = [[ARR[:]]]
# then make empty row for the rest
output.append([[] for _ in range(how_many_rows - 1)])
"""

output = [[] for _ in range(how_many_rows)]
output[0].append(ARR[:])

""" Merge Sort Functions. """
def merge(left, right):
    # initializing temps
    i = 0
    j = 0
    results = []

    # initial merging until one runs out
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            results.append(left[i])
            i += 1
        else:
            results.append(right[j])
            j += 1

    # adding leftovers
    while i < len(left):
        results.append(left[i])
        i += 1
    while j < len(right):
        results.append(right[j])
        j += 1

    return results


def mergeSort(arr, current_row):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2

    left = arr[:mid]
    right = arr[mid:]

    output[current_row].append(left)
    output[current_row].append(right)

    left = mergeSort(left, current_row + 1)
    right = mergeSort(right, current_row + 1)
    merged = merge(left, right)
    output[how_many_rows - current_row].append(merged)
    return merged

def fill_in_missing_entries():
    # The only rows where we can have missing elements is in the middle row (where everything is by itself)
    # or the row after where they are merging things for the first time. Therefore, just compare those rows with
    # the rows above them to fill in any blanks.

    counter = 0 # keep a counter b/c each insert means we have to move it over by one.
    middle_row_index = (how_many_rows // 2) # to quickly find middle rows.

    for row in range(middle_row_index, middle_row_index + 2):

        for segment in range(len(output[middle_row_index - 1])):
            
            for element in range(len(output[middle_row_index - 1][segment])):

                # Start above the middle row, check to see the element is in the row below.
                done = False
                for below_segment in output[row]:
                    
                    for below_element in below_segment:
                        if output[middle_row_index - 1][segment][element] == below_element:
                            done = True
                            break

                # if it's not in the row below, we need to add it.
                if not done:

                    # we know the missing element is at element in segment, so we add it to the next row
                    # and increment the counter
                    output[row].insert(segment + counter, output[middle_row_index - 1][segment])

                    # we only need the counter for the middle row
                    if row == middle_row_index:
                        counter += 1
        counter = 0
                        

mergeSort(ARR, 1)
fill_in_missing_entries()
print(output)

class Test(Scene):
    def construct(self):
        title = Text("Hello World")
        self.play(Write(title))
        self.wait(2)