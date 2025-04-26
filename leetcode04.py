from manim import *
class MatrixRotation(Scene):
    def construct(self):
        # Title and introduction
        title = Text("Matrix Rotation (90° Clockwise)", font_size=48)
        subtitle = Text("In-place algorithm visualization", font_size=32)
        
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        self.play(Write(subtitle.next_to(title, DOWN)))
        self.wait(2)
        self.play(FadeOut(subtitle))
        
        # Problem statement
        problem = Text("Given an n×n matrix, rotate it 90° clockwise in-place", font_size=32)
        self.play(Write(problem.next_to(title, DOWN)))
        self.wait(2)
        self.play(FadeOut(problem))
        
        # Create a 4x4 matrix for demonstration
        matrix_values = [
            [5, 1, 9, 11],
            [2, 4, 8, 10],
            [13, 3, 6, 7],
            [15, 14, 12, 16]
        ]
        
        # Create matrix visualization
        matrix = self.create_matrix(matrix_values)
        matrix.move_to(ORIGIN)
        
        # Show original matrix
        original_label = Text("Original Matrix", font_size=36).next_to(matrix, UP)
        self.play(Write(original_label))
        self.play(FadeIn(matrix))
        self.wait(2)
        
        # Explain the rotation formula
        formula_text = Text("Rotation Formula:", font_size=32)
        formula = MathTex("(row, col) \\rightarrow (col, n-1-row)").scale(1.2)
        formula_group = VGroup(formula_text, formula).arrange(DOWN)
        formula_group.next_to(matrix, DOWN, buff=1)
        
        self.play(Write(formula_group))
        self.wait(2)
        self.play(FadeOut(formula_group))
        
        # Clear for algorithm explanation
        self.play(
            FadeOut(original_label),
            title.animate.to_edge(UP)
        )
        
        # Explain the layer-by-layer approach
        approach_text = Text("Layer-by-Layer Rotation Approach", font_size=36)
        approach_text.next_to(title, DOWN)
        self.play(Write(approach_text))
        self.wait(1)
        
        # Visualize layers
        self.explain_layers(matrix, matrix_values)
        self.play(FadeOut(approach_text))
        
        # Explain the algorithm with step-by-step rotation
        self.explain_rotation_algorithm(matrix, matrix_values)
        
        # Conclusion
        conclusion = Text("Time Complexity: O(n²)", font_size=32).to_edge(DOWN)
        space_complexity = Text("Space Complexity: O(1) - In-place", font_size=32).next_to(conclusion, UP)
        
        self.play(Write(space_complexity))
        self.play(Write(conclusion))
        self.wait(3)
        
        self.play(
            FadeOut(title),
            FadeOut(matrix),
            FadeOut(conclusion),
            FadeOut(space_complexity)
        )
        
        final_title = Text("Thank you for watching!", font_size=48)
        self.play(Write(final_title))
        self.wait(2)
    
    def create_matrix(self, values):
        n = len(values)
        cells = VGroup()
        
        for i in range(n):
            for j in range(n):
                cell = Square(side_length=1)
                cell.set_stroke(WHITE, 2)
                text = Text(str(values[i][j]), font_size=24)
                text.move_to(cell.get_center())
                cell_group = VGroup(cell, text)
                cell_group.move_to([j, -i, 0])  # Position in grid
                cells.add(cell_group)
        
        return cells
    
    def explain_layers(self, matrix, values):
        n = len(values)
        layers = n // 2
        
        for layer in range(layers):
            # Highlight current layer
            layer_cells = VGroup()
            
            # Add top row of this layer
            for j in range(layer, n-layer):
                idx = layer * n + j
                layer_cells.add(matrix[idx])
            
            # Add right column of this layer (excluding the corner already added)
            for i in range(layer+1, n-layer):
                idx = i * n + (n-layer-1)
                layer_cells.add(matrix[idx])
            
            # Add bottom row of this layer (excluding the corner already added)
            for j in range(n-layer-2, layer-1, -1):
                idx = (n-layer-1) * n + j
                layer_cells.add(matrix[idx])
            
            # Add left column of this layer (excluding the corner already added)
            for i in range(n-layer-2, layer, -1):
                idx = i * n + layer
                layer_cells.add(matrix[idx])
            
            layer_text = Text(f"Layer {layer+1}", font_size=28)
            layer_text.to_edge(LEFT).shift(UP * 2)
            
            # Highlight the layer
            self.play(
                Write(layer_text),
                *[cell[0].animate.set_fill(YELLOW, opacity=0.3) for cell in layer_cells]
            )
            self.wait(1)
            
            # Unhighlight the layer
            self.play(
                FadeOut(layer_text),
                *[cell[0].animate.set_fill(opacity=0) for cell in layer_cells]
            )
    
    def explain_rotation_algorithm(self, matrix, values):
        n = len(values)
        
        algorithm_title = Text("In-place Rotation Algorithm", font_size=36)
        algorithm_title.next_to(matrix, UP)
        
        self.play(Write(algorithm_title))
        self.wait(1)
        
        # Show pseudocode
        pseudocode = VGroup(
            Text("for layer = 0 to n/2 - 1:", font_size=24),
            Text("    first = layer", font_size=24),
            Text("    last = n - 1 - layer", font_size=24),
            Text("    for i = first to last - 1:", font_size=24),
            Text("        temp = matrix[first][i]", font_size=24),
            Text("        matrix[first][i] = matrix[n-1-i][first]", font_size=24),
            Text("        matrix[n-1-i][first] = matrix[last][n-1-i]", font_size=24),
            Text("        matrix[last][n-1-i] = matrix[i][last]", font_size=24),
            Text("        matrix[i][last] = temp", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        pseudocode.scale(0.7).to_edge(RIGHT)
        self.play(Write(pseudocode))
        self.wait(2)
        
        # Perform the rotation layer by layer
        for layer in range(n // 2):
            first = layer
            last = n - 1 - layer
            
            layer_text = Text(f"Layer {layer+1}: first={first}, last={last}", font_size=28)
            layer_text.next_to(matrix, DOWN, buff=1)
            self.play(Write(layer_text))
            self.wait(1)
            
            # Rotate each element in the current layer
            for i in range(first, last):
                # Get indices for the four cells involved in this rotation
                top_idx = first * n + i
                left_idx = (n-1-i) * n + first
                bottom_idx = last * n + (n-1-i)
                right_idx = i * n + last
                
                # Get the cells
                top = matrix[top_idx]
                left = matrix[left_idx]
                bottom = matrix[bottom_idx]
                right = matrix[right_idx]
                
                cells = [top, left, bottom, right]
                
                # Highlight the cells with different colors
                colors = [RED, BLUE, GREEN, YELLOW]
                self.play(*[cell[0].animate.set_fill(color, opacity=0.3) for cell, color in zip(cells, colors)])
                
                # Show temp variable
                temp_text = Text(f"temp = {top[1].text}", font_size=24)
                temp_text.next_to(layer_text, DOWN)
                self.play(Write(temp_text))
                
                # Store original values
                values = [cell[1].text for cell in cells]
                
                # Step 1: top = left
                step1_text = Text(f"matrix[{first}][{i}] = matrix[{n-1-i}][{first}]", font_size=24)
                step1_text.next_to(temp_text, DOWN)
                
                # Create a copy for animation
                moving_text = Text(values[1], font_size=24)
                moving_text.move_to(left.get_center())
                
                self.play(Write(step1_text))
                self.play(FadeIn(moving_text))
                self.play(moving_text.animate.move_to(top.get_center()))
                self.play(FadeOut(top[1]))
                
                # Update the cell
                new_text = Text(values[1], font_size=24)
                new_text.move_to(top.get_center())
                top[1] = new_text
                
                self.play(
                    FadeIn(new_text),
                    FadeOut(moving_text)
                )
                self.play(FadeOut(step1_text))
                
                # Step 2: left = bottom
                step2_text = Text(f"matrix[{n-1-i}][{first}] = matrix[{last}][{n-1-i}]", font_size=24)
                step2_text.next_to(temp_text, DOWN)
                
                # Create a copy for animation
                moving_text = Text(values[2], font_size=24)
                moving_text.move_to(bottom.get_center())
                
                self.play(Write(step2_text))
                self.play(FadeIn(moving_text))
                self.play(moving_text.animate.move_to(left.get_center()))
                self.play(FadeOut(left[1]))
                
                # Update the cell
                new_text = Text(values[2], font_size=24)
                new_text.move_to(left.get_center())
                left[1] = new_text
                
                self.play(
                    FadeIn(new_text),
                    FadeOut(moving_text)
                )
                self.play(FadeOut(step2_text))
                
                # Step 3: bottom = right
                step3_text = Text(f"matrix[{last}][{n-1-i}] = matrix[{i}][{last}]", font_size=24)
                step3_text.next_to(temp_text, DOWN)
                
                # Create a copy for animation
                moving_text = Text(values[3], font_size=24)
                moving_text.move_to(right.get_center())
                
                self.play(Write(step3_text))
                self.play(FadeIn(moving_text))
                self.play(moving_text.animate.move_to(bottom.get_center()))
                self.play(FadeOut(bottom[1]))
                
                # Update the cell
                new_text = Text(values[3], font_size=24)
                new_text.move_to(bottom.get_center())
                bottom[1] = new_text
                
                self.play(
                    FadeIn(new_text),
                    FadeOut(moving_text)
                )
                self.play(FadeOut(step3_text))
                
                # Step 4: right = temp (original top)
                step4_text = Text(f"matrix[{i}][{last}] = temp", font_size=24)
                step4_text.next_to(temp_text, DOWN)
                
                # Create a copy for animation
                moving_text = Text(values[0], font_size=24)
                moving_text.move_to(temp_text.get_center())
                
                self.play(Write(step4_text))
                self.play(FadeIn(moving_text))
                self.play(moving_text.animate.move_to(right.get_center()))
                self.play(FadeOut(right[1]))
                
                # Update the cell
                new_text = Text(values[0], font_size=24)
                new_text.move_to(right.get_center())
                right[1] = new_text
                
                self.play(
                    FadeIn(new_text),
                    FadeOut(moving_text)
                )
                
                # Clean up
                self.play(
                    FadeOut(temp_text),
                    FadeOut(step4_text),
                    *[cell[0].animate.set_fill(opacity=0) for cell in cells]
                )
                self.wait(0.5)
            
            self.play(FadeOut(layer_text))
            self.wait(1)
        
        # Show the final rotated matrix
        rotated_label = Text("Rotated Matrix", font_size=36).next_to(matrix, UP)
        self.play(
            FadeOut(algorithm_title),
            FadeOut(pseudocode),
            Write(rotated_label)
        )
        self.wait(2)
