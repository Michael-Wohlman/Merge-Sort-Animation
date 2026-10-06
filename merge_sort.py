from manim import *

""" Variables to change (default is ARR = [38, 27, 43, 3, 9, 82, 10])"""
ARR = [1, 2, 3, 4, 5]


""" Initializing the Output array with empty rows. """
# One row per split/merge depth, plus the initial array.
how_many_rows = 2 * (max(1, len(ARR)) - 1).bit_length() + 1

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

    # Check all types before attempting any ordering comparisons.
    for i in range(1, len(arr)):
        if type(arr[i]) is not type(arr[0]):
            results[1] = i
            return results

    # A singleton is already sorted, as are arrays of equal values.
    if all(arr[i - 1] <= arr[i] for i in range(1, len(arr))):
        results[2] = 1

    return results


class Test(Scene):
    def construct(self):
        box_size = 0.9
        gap = 0.12
        array_boxes = VGroup()

        for value in ARR:
            box = Square(side_length=box_size, color=BLUE)
            box.set_fill(BLUE, opacity=0.15)
            label = Text(str(value), font_size=30)
            if label.width > box_size * 0.75:
                label.scale_to_fit_width(box_size * 0.75)
            label.move_to(box.get_center())
            array_boxes.add(VGroup(box, label))

        array_boxes.arrange(RIGHT, buff=gap)
        if array_boxes.width > config.frame_width - 1:
            array_boxes.scale_to_fit_width(config.frame_width - 1)
        array_boxes.move_to(ORIGIN)

        if len(array_boxes):
            self.play(
                LaggedStart(
                    *(FadeIn(cell, shift=UP * 0.2) for cell in array_boxes),
                    lag_ratio=0.15,
                ),
                run_time=1.5,
            )
        else:
            self.play(FadeIn(Text("[]", font_size=36).move_to(ORIGIN)))

        check_rows = VGroup()
        check_boxes = []
        for name in ("Non-Empty", "Same Type", "Already sorted"):
            checkbox = Square(side_length=0.35, color=WHITE)
            label = Text(name, font_size=24)
            row = VGroup(checkbox, label).arrange(RIGHT, buff=0.2)
            check_rows.add(row)
            check_boxes.append(checkbox)

        check_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        check_rows.next_to(array_boxes if len(array_boxes) else ORIGIN, UP, buff=0.6)
        self.play(FadeIn(check_rows))

        results = initial_checks(ARR)
        failure_messages = (
            "The array is empty.",
            "All elements must have the same type.",
            "The array is already sorted.",
        )
        for index, (checkbox, result) in enumerate(zip(check_boxes, results)):
            self.wait(0.5)
            center = checkbox.get_center()
            if result == -1:
                # Draw the mark with lines so it does not depend on font glyphs.
                mark = VMobject(color=GREEN, stroke_width=4)
                mark.set_points_as_corners([
                    center + LEFT * 0.11,
                    center + LEFT * 0.025 + DOWN * 0.09,
                    center + RIGHT * 0.12 + UP * 0.10,
                ])
            else:
                mark = VGroup(
                    Line(center + UL * 0.10, center + DR * 0.10, color=RED),
                    Line(center + DL * 0.10, center + UR * 0.10, color=RED),
                )
            self.play(Create(mark), run_time=0.4)
            if result != -1:
                message = Text(failure_messages[index], font_size=24, color=RED)
                message.next_to(array_boxes if len(array_boxes) else ORIGIN, DOWN, buff=0.6)
                self.play(FadeIn(message))
                self.wait(2)
                return

        # Only build sorting data after every check passes.
        for row in output:
            row.clear()
        output[0].append(ARR[:])
        mergeSort(ARR, 1)
        fill_in_missing_entries()
        self.wait(2)
