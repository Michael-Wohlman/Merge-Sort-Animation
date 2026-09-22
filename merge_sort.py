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

    # I know what your thinking. "Five for loops?! is this dev insane?!"
    # Maybe. But it is not O(n^5). The five for loops are to deal with the complex data.
    # We have elements of a list that are themselves lists, which contain subarrays.
    # The nested for loops are really just for accessing these rows of subarrays, and each row of subarrays in length n.
    # So we compare the row above middle to the middle row, then the row above middle to the row below middle.
    # Which makes this O(4*n) = O(n) technically.

    # For example, we could have [
    # [[5,2], [1], [3,4]],        above middle
    # [[5], [2], [3], [4]],       middle
    # [[2, 5], [3,4]]             below middle
    # if we want to fill in the missing [1]s, we need to compare the above to middle and above to below.

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

def initial_checks(arr):

    """ Returns [empty, same type, already sorted]. -1 means it passes, positive means it fails and we do not sort """
    results = [-1, -1, -1]

    # check if arr is empty
    if len(arr) <= 0:
        results[0] = 1
        return results

    # if arr only has 1 element, it is already sorted.
    if len(arr) == 1:
        results[1] = 1
        return results

    # otherwise check every element to see if it is the same type as the previous one and if arr is already sorted
    sorted = True
    for i in range(1, len(arr)):
        # compare the types
        if type(arr[i-1]) == type(arr[i]):

            # if we still think its sorted, check if prev is greater than current to confirm its not sorted
            if sorted == True and arr[i-1] > arr [i]:
                sorted = False
        
        # if they are different types, then mark that in results and stop searching.
        else:
            results[1] = i
            return results

    if sorted:
        results[2] = 1

    return results


initial_check_results = initial_checks(ARR)
mergeSort(ARR, 1)
fill_in_missing_entries()
print(output)

class Test(Scene):
    def construct(self):
        title = Text("Hello World")
        self.play(Write(title))
        self.wait(2)