from manim import *
import os
class MatrixRotationWithMath(Scene):
    def construct(self):
        # Title
        title = Tex(r"\textbf{Matrix Rotation (90° Clockwise)}", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP))
        self.play(FadeOut(title))

        # Mathematical Explanation
        self.explain_math()

        # Algorithmic Explanation
        self.explain_algorithm()

        # Example 1 Matrices (3×3)
        example1_initial = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        example1_transposed = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        example1_rotated = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

        # Example 2 Matrices (4×4)
        example2_initial = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
        example2_transposed = [[5, 2, 13, 15], [1, 4, 3, 14], [9, 8, 6, 12], [11, 10, 7, 16]]
        example2_rotated = [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]

        # Show Example 1
        example1_title = Tex(r"\textbf{Example 1}", font_size=42)
        example1_title.to_edge(UP, buff=0.5)
        self.play(Write(example1_title))
        self.show_example(example1_initial, example1_transposed, example1_rotated)

        self.play(FadeOut(example1_title))
        self.clear_screen()

        # Show Example 2
        example2_title = Tex(r"\textbf{Example 2}", font_size=42)
        example2_title.to_edge(UP, buff=0.8)
        self.play(Write(example2_title))
        self.show_example(example2_initial, example2_transposed, example2_rotated)

        self.wait(3)

        # Show Code Explanation
        self.show_code()

    def explain_math(self):
        """Displays mathematical explanation"""
        math_text = Tex(r"\textbf{Mathematical Steps:}", font_size=42).to_edge(UP)
        step1 = Tex(r"1. \textbf{Transpose} the matrix: $A[i][j] \leftrightarrow A[j][i]$", font_size=36)
        step2 = Tex(r"2. \textbf{Reverse each row}: $A[i] = A[i][::-1]$", font_size=36)
        steps = VGroup(step1, step2).arrange(DOWN, buff=0.5)

        self.play(Write(math_text))
        self.wait(1)
        self.play(FadeIn(steps))
        self.wait(2)
        self.play(FadeOut(math_text), FadeOut(steps))

    def explain_algorithm(self):
        """Displays algorithm explanation"""
        algo_text = Tex(r"\textbf{Algorithm for 90° Rotation}", font_size=42).to_edge(UP)
        step1 = Tex(r"1. Iterate over matrix and swap $A[i][j]$ with $A[j][i]$.", font_size=36)
        step2 = Tex(r"2. Reverse every row of the transposed matrix.", font_size=36)
        steps = VGroup(step1, step2).arrange(DOWN, buff=0.5)

        self.play(Write(algo_text))
        self.wait(1)
        self.play(FadeIn(steps))
        self.wait(2)
        self.play(FadeOut(algo_text), FadeOut(steps))

    def show_example(self, initial_matrix, transposed_matrix, rotated_matrix):
        """Handles the step-by-step process for a single example"""
        # Show Initial Matrix
        matrix_mob = self.create_matrix(initial_matrix, "Initial Matrix")
        self.play(FadeIn(matrix_mob))
        self.wait(2)

        # Step 1: Transpose
        step_text = self.show_step_text("Step 1: Transpose the Matrix")
        self.wait(1)

        swap_list = self.get_transpose_swaps(len(initial_matrix))
        for r1, c1, r2, c2 in swap_list:
            self.swap_elements(matrix_mob, r1, c1, r2, c2, len(initial_matrix))
            self.wait(1.5)

        self.play(FadeOut(step_text))
        self.wait(1)

        # Step 2: Reverse Rows
        step_text = self.show_step_text("Step 2: Reverse Each Row")
        self.wait(1)

        for row in range(len(initial_matrix)):
            self.reverse_row(matrix_mob, row, len(initial_matrix))
            self.wait(1.5)

        self.play(FadeOut(step_text))
        self.wait(2)

    def show_step_text(self, text):
        """Display step-by-step text instructions properly without overlapping."""
        step_text = Tex(rf"\textbf{{{text}}}", font_size=40)
        step_text.to_edge(DOWN, buff=1.5)  # Ensure proper positioning
        self.play(Write(step_text))
        return step_text  # Return so we can remove it before showing the next one

    def show_code(self):
        """Displays Python and C++ code"""
        code_text = Tex(r"\textbf{Python and C++ Code}", font_size=42).to_edge(UP)
        python_code = Tex(r"""
        \textbf{Python:}
        def rotate(matrix):
            n = len(matrix)
            for i in range(n):
                for j in range(i, n):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            for row in matrix:
                row.reverse()
        """, font_size=32)

        '''cpp_code = Tex(r"""
        \textbf{C++:}
        void rotate(vector<vector<int>>& matrix) {
            int n = matrix.size();
            for (int i = 0; i < n; i++) {
                for (int j = i; j < n; j++) {
                    swap(matrix[i][j], matrix[j][i]);
                }
            }
            for (int i = 0; i < n; i++) {
                reverse(matrix[i].begin(), matrix[i].end());
            }
        }
        """, font_size=32)'''

        codes = VGroup(python_code).arrange(DOWN, buff=1.0)

        self.play(Write(code_text))
        self.wait(1)
        self.play(FadeIn(codes))
        self.wait(3)
        self.play(FadeOut(code_text), FadeOut(codes))


    def create_matrix(self, matrix, title):
        """Create a matrix with elements and a surrounding rectangle."""
        elements = VGroup()
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                element = Tex(str(matrix[i][j]), font_size=36)
                element.move_to(np.array([j - (n-1)/2, (n-1)/2 - i, 0]))
                elements.add(element)

        matrix_box = SurroundingRectangle(elements, color=WHITE, buff=0.2)
        return VGroup(Tex(title, font_size=36), elements, matrix_box)
    
    def swap_elements(self, matrix_mob, r1, c1, r2, c2, n):
        """Swap two elements in the matrix with an animation."""
        elements = matrix_mob[1]
        idx1 = r1 * n + c1
        idx2 = r2 * n + c2

        rect1 = SurroundingRectangle(elements[idx1], color=YELLOW, buff=0.1)
        rect2 = SurroundingRectangle(elements[idx2], color=YELLOW, buff=0.1)

        self.play(Create(rect1), Create(rect2))
        self.wait(0.5)

        self.play(elements[idx1].animate.move_to(elements[idx2].get_center()),
                  elements[idx2].animate.move_to(elements[idx1].get_center()), run_time=1)

        self.play(FadeOut(rect1), FadeOut(rect2))

        elements[idx1], elements[idx2] = elements[idx2], elements[idx1]

    def reverse_row(self, matrix_mob, row, n):
        """Reverse a row element by element."""
        elements = matrix_mob[1]

        left_idx = row * n
        right_idx = row * n + (n - 1)

        while left_idx < right_idx:
            rect1 = SurroundingRectangle(elements[left_idx], color=RED, buff=0.1)
            rect2 = SurroundingRectangle(elements[right_idx], color=RED, buff=0.1)

            self.play(Create(rect1), Create(rect2))
            self.wait(0.5)

            self.play(elements[left_idx].animate.move_to(elements[right_idx].get_center()),
                      elements[right_idx].animate.move_to(elements[left_idx].get_center()), run_time=1)

            self.play(FadeOut(rect1), FadeOut(rect2))

            elements[left_idx], elements[right_idx] = elements[right_idx], elements[left_idx]

            left_idx += 1
            right_idx -= 1

    def get_transpose_swaps(self, n):     
        swaps = []
        for i in range(n):
            for j in range(i, n):
                swaps.append((i, j, j, i))
        return swaps
    
    def clear_screen(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

# Run the scene
if __name__ == "__main__":
    os.system("manim -pqh mce/lc04_02.py MatrixRotationWithMath")
