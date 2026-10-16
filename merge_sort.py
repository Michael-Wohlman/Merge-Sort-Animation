from email import message

from manim import *  # pyright: ignore[reportMissingImports]

""" Variables to change """
# Input array (default is ARR = [38, 27, 43, 3, 9, 82, 10])
ARR = [38, 27, 43, 3, 9, 82, 10]

# Speed of animation (1 = normal, 2 = double, etc.)
ANIM_SPEED = 2



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
    """Carry every singleton through the deepest split and first merge."""
    middle_row_index = how_many_rows // 2
    if middle_row_index == 0:
        return

    # At this depth each segment has one or two elements. Rebuild these
    # two rows from their parent segments, preserving position and duplicates.
    # A singleton stays in place while a pair splits and then merges.
    parent_row = output[middle_row_index - 1]
    output[middle_row_index] = [
        [value] for segment in parent_row for value in segment
    ]
    output[middle_row_index + 1] = [
        sorted(segment) for segment in parent_row
    ]


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


# Visual constants
cell_spacing = 0.05
cell_size =  min(.7, 12 / ((0.7 * len(ARR)) + (cell_spacing * len(ARR))))
row_spacing = 1.3
font_size = 40 * cell_size
ANIMATION_SPEED_MULT = 1 / ANIM_SPEED
STEP_RUN_TIME = 1               * ANIMATION_SPEED_MULT
STEP_PAUSE_TIME = 2             * ANIMATION_SPEED_MULT
CHECK_PAUSE_TIME = 1.5          * ANIMATION_SPEED_MULT
CHECK_MARK_RUN_TIME = 0.8       * ANIMATION_SPEED_MULT
CHECK_RESULT_HOLD_TIME = 2      * ANIMATION_SPEED_MULT
CHECK_FAILURE_HOLD_TIME = 4     * ANIMATION_SPEED_MULT
SPLIT_TRANSITION_PAUSE_TIME = 3 * ANIMATION_SPEED_MULT
MERGE_FOCUS_RUN_TIME = 0.5      * ANIMATION_SPEED_MULT
MERGE_FOCUS_PAUSE_TIME = 1      * ANIMATION_SPEED_MULT
MERGE_ELEMENT_PAUSE_TIME = 0.3  * ANIMATION_SPEED_MULT
SPLIT_EXPLANATIONS = [
    "Divide the original array into two halves.",
    "Continue dividing each subarray into smaller pieces.",
    "Split until every subarray contains only one element, and is therefore technically sorted."
]
MERGE_EXPLANATIONS = [
    "Begin merging individual elements into sorted subarrays.",
    "Continue combining smaller sorted subarrays.",
    "Merge the remaining sorted halves into the final sorted array."
]
color_default = WHITE
color_compare = YELLOW
color_merge_focus = BLUE
color_placed = GREEN
color_split_line = GRAY


def make_cell(value, border_color = color_default, text_color = WHITE):
    box = Square(side_length = cell_size, color = border_color)
    number = Text(str(value), font_size = font_size, color = text_color)
    number.move_to(box.get_center())
    return VGroup(box, number)


def make_array(values, border_color = color_default, text_color=WHITE):
    cells = VGroup(*(make_cell(v, border_color, text_color) for v in values))
    cells.arrange(RIGHT, buff = cell_spacing)
    return cells


def make_row(row_data, border_color = color_default):
    # [[38, 27], [9]] becomes one array group per sub-array
    row = VGroup(*(make_array(sub, border_color=border_color) for sub in row_data))
    row.arrange(RIGHT, buff =0.6)
    return row


class MergeSortVisualization(Scene):
    def move_merge_cell(self, cell, position):
        # Place each number directly into the next row below its input.
        self.play(cell.animate.move_to(position), run_time=STEP_RUN_TIME)
        self.wait(MERGE_ELEMENT_PAUSE_TIME)

    def animate_initial_checks(self, array_display):
        introduction = Text(
            "Before we can sort this array,\n"
            "We need to go through some edge cases first.",
            font_size=24,
        )
        if introduction.width > config.frame_width - 1:
            introduction.scale_to_fit_width(config.frame_width - 1)
        introduction.next_to(array_display, UP, buff=0.6)
        self.play(FadeIn(introduction), run_time=1.5)
        self.wait(5)

        check_rows = VGroup()
        check_boxes = []
        check_marks = VGroup()
        for name in ("Non-Empty", "Same Type", "Not Already sorted"):
            checkbox = Square(side_length=0.35, color=WHITE)
            label = Text(name, font_size=24)
            row = VGroup(checkbox, label).arrange(RIGHT, buff=0.2)
            check_rows.add(row)
            check_boxes.append(checkbox)

        check_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        check_rows.next_to(array_display, UP, buff=0.6)
        self.play(FadeOut(introduction), FadeIn(check_rows), run_time=2)

        results = initial_checks(ARR)
        failure_messages = (
            "The array is empty.",
            "All elements must have the same type.",
            "The array is already sorted.",
        )
        for index, (checkbox, result) in enumerate(zip(check_boxes, results)):
            self.wait(CHECK_PAUSE_TIME)
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
            check_marks.add(mark)
            mark_animations = [Create(mark)]
            if result != -1 and index == 1:
                # The type check returns the index of the first mismatched element.
                mark_animations.append(array_display[result].animate.set_color(RED))
            elif result != -1 and index == 0:
                mark_animations.append(array_display.animate.set_color(RED))
            self.play(*mark_animations, run_time=CHECK_MARK_RUN_TIME)
            if result != -1:
                message = Text(failure_messages[index], font_size=24, color=RED)
                message.next_to(array_display, DOWN, buff=0.6)
                self.play(FadeIn(message))
                self.wait(CHECK_FAILURE_HOLD_TIME)
                return False

        self.wait(CHECK_RESULT_HOLD_TIME)
        sort_message = Text("Now we begin the sort!", font_size=24)
        sort_message.move_to(check_rows.get_center())
        self.play(
            FadeOut(check_rows), FadeOut(check_marks), FadeIn(sort_message),
            run_time=2,
        )
        self.wait(4)
        self.play(FadeOut(sort_message), run_time=1.5)
        return True

    def construct(self):
        # Title
        title = Text("Merge Sort", font_size = 38)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Original cells
        cells = VGroup()

        # Keep track of the value belonging to each cell
        cell_data = []

        for value in ARR:

            cell = make_cell(value)

            cells.add(cell)

            cell_data.append({
                "value": value,
                "cell": cell
            })

        cells.arrange(RIGHT, buff=cell_spacing)

        # Fit large arrays on screen if necessary
        if cells.width > config.frame_width - 2:
            cells.scale_to_fit_width(config.frame_width - 2)

        cells.move_to(ORIGIN)

        # Labels
        input_label = Text("INPUT", font_size = 20, color = GRAY)
        array_display = cells if len(cells) else Text("[]", font_size=36).move_to(ORIGIN)
        input_label.next_to(array_display, LEFT, buff = 0.5)
        phase_label = None
        self.play(FadeIn(array_display), FadeIn(input_label))
        self.wait(1)

        if not self.animate_initial_checks(array_display):
            return

        # Only build sorting data after every initial check passes.
        for row in output:
            row.clear()
        output[0].append(ARR[:])
        mergeSort(ARR, 1)
        fill_in_missing_entries()

        # INPUT label is no longer necessary once animation starts
        # Reuse a fixed input row and a working row below it.
        top_y = title.get_bottom()[1] - 0.5 - cells.height / 2
        bottom_y = -config.frame_height / 2 + 1.1 + cells.height / 2
        level_spacing = min(row_spacing, top_y - bottom_y)
        self.play(
            FadeOut(input_label),
            cells.animate.move_to(UP * top_y),
            run_time=1.5,
        )
        self.wait(SPLIT_TRANSITION_PAUSE_TIME)
       
        # Determine where splitting changes into merging
        middle_row_index = how_many_rows // 2

        #Track the current explanation for each phase
        split_step = 0
        merge_step = 0
        # Animate each row generated by merge sort
        for row_index in range(1, len(output)):

            row_data = output[row_index]

            # Some output rows may be unused
            if len(row_data) == 0:
                continue

            # Update SPLIT / MERGE label
            if row_index <= middle_row_index:
                explanation_index = min(split_step, len(SPLIT_EXPLANATIONS) - 1)

                message = SPLIT_EXPLANATIONS[explanation_index]
                new_phase_label = Text(message, font_size = 24, color = YELLOW)
                split_step += 1

            else:
                explanation_index = min(merge_step, len(MERGE_EXPLANATIONS) - 1)

                message = MERGE_EXPLANATIONS[explanation_index]
                new_phase_label = Text(message, font_size =  24, color = GREEN)
                merge_step += 1

            if new_phase_label.width > config.frame_width - 1:
                new_phase_label.scale_to_fit_width(config.frame_width - 1)
                # This line determines where the merge explanations show on screen
                new_phase_label.to_edge(DOWN, buff = 2)

            if phase_label is None:
                self.play(FadeIn(new_phase_label), run_time=1)
                phase_label = new_phase_label
                self.wait(SPLIT_TRANSITION_PAUSE_TIME)
            else: 
                self.play(FadeOut(phase_label), FadeIn(new_phase_label), run_time=0.3)
                phase_label = new_phase_label

            # Create a TEMPORARY row (which isn't shown)
            # Only used to find where every cell should move        
            target_row = make_row(row_data, border_color = color_default)
            target_row.move_to(ORIGIN)

            # Make sure the target layout fits on screen
            if target_row.width > config.frame_width - 1:
                target_row.scale_to_fit_width(config.frame_width - 1)

            # Build every split or merge in the same lower working row.
            target_row.move_to(UP * (top_y - level_spacing))

            # Organize existing cells by their values
            available_cells = {}

            for item in cell_data:

                value = item["value"]
                cell = item["cell"]

                if value not in available_cells:
                    available_cells[value] = []

                available_cells[value].append(cell)

            # Sort duplicate values by their current left-to-right position.
            for value in available_cells:

                available_cells[value].sort(key = lambda c: c.get_center()[0])

            # Match all cells before moving them, including duplicate values.
            matched_groups = []

            for sub_array_values, target_sub_array in zip(row_data, target_row):
                matched_cells = []
                for value, target_cell in zip(sub_array_values, target_sub_array):

                    # Grab existing cell containing this value
                    current_cell = available_cells[value].pop(0)

                    matched_cells.append((current_cell, target_cell.get_center()))
                matched_groups.append(matched_cells)

            if row_index <= middle_row_index:
                # Split the whole row together as before.
                self.play(*[
                    cell.animate.move_to(position)
                    for group in matched_groups
                    for cell, position in group
                ], run_time=STEP_RUN_TIME)
                self.wait(STEP_PAUSE_TIME)
            else:
                # Focus on each group, including carried singletons, from left to right.
                for group in matched_groups:
                    self.play(*[
                        cell.animate.set_color(color_merge_focus)
                        for cell, _ in group
                    ], run_time=MERGE_FOCUS_RUN_TIME)
                    self.wait(MERGE_FOCUS_PAUSE_TIME)
                    # Destination order is sorted, so place one number at a time.
                    for cell, position in group:
                        self.move_merge_cell(cell, position)
                    self.wait(STEP_PAUSE_TIME)
                    self.play(*[
                        cell.animate.set_color(color_default)
                        for cell, _ in group
                    ], run_time=MERGE_FOCUS_RUN_TIME)

            # Raise the completed row together before starting the next step.
            self.play(*[
                item["cell"].animate.shift(UP * level_spacing)
                for item in cell_data
            ], run_time=STEP_RUN_TIME)
            self.wait(MERGE_FOCUS_PAUSE_TIME)

        
        # Final sorted-array highlight
        if phase_label is not None:
            self.play(FadeOut(phase_label), run_time=0.3)
        self.play(*[item["cell"].animate.set_color(color_placed) for item in cell_data], run_time=STEP_RUN_TIME)
        self.wait(2)
