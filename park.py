from manim import (
    Scene, VGroup, Tex, MathTex, Axes, ParametricFunction, Dot, MoveAlongPath,
    FadeIn, Write, Create, FadeOut, ReplacementTransform, GrowArrow,
    BLUE, YELLOW, RED, GREEN, GRAY, WHITE, UP, DOWN, LEFT, RIGHT, PI,
    np, ORIGIN, linear, ValueTracker, always_redraw, Circle, Arrow, Line,
    Arc, Text
)

class ParkTransformVisualization(Scene):
    def construct(self):
        # ---------------------- 1. Introduction ----------------------
        title = Tex(r"\textbf{Understanding the Park Transform}", font_size=60, color=BLUE).to_edge(UP)
        subtitle = Tex(r"A powerful tool for AC motor control!", font_size=40, color=YELLOW).next_to(title, DOWN)
        
        self.play(Write(title, run_time=1.5), FadeIn(subtitle, shift=UP))
        
        overview = VGroup(
            Tex(r"$\bullet$ \text{Three-phase electrical systems}", font_size=32),
            Tex(r"$\bullet$ \text{Clarke Transform ($abc \to \alpha\beta$)}", font_size=32),
            Tex(r"$\bullet$ \text{Park Transform ($\alpha\beta \to dq$)}", font_size=32),
            Tex(r"$\bullet$ \text{Applications in motor control}", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subtitle, DOWN, buff=0.5)
        
        self.play(FadeIn(overview, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(overview))

        # -------------------- 2. Three-Phase System -------------------
        three_phase_title = Tex(r"\textbf{Three-Phase AC System}", font_size=48, color=BLUE).to_edge(UP)
        three_phase_subtitle = Tex(r"$120^\circ$ \text{ phase-shifted sinusoidal waveforms}", font_size=32).next_to(three_phase_title, DOWN)
        
        time_axes = Axes(
            x_range=[0, 2*PI, PI/2], y_range=[-1.5, 1.5, 0.5],
            x_length=10, y_length=4, axis_config={"color": GRAY},
            x_axis_config={"include_tip": False}, y_axis_config={"include_tip": False}
        ).shift(DOWN)
        
        time_labels = VGroup(
            Tex(r"\text{Time}", font_size=24).next_to(time_axes.x_axis, DOWN, buff=0.2),
            Tex(r"\text{Amplitude}", font_size=24).next_to(time_axes.y_axis, LEFT, buff=0.2)
        )
        
        x_labels = VGroup(
            MathTex(r"0", font_size=20).next_to(time_axes.c2p(0, 0), DOWN, buff=0.1),
            MathTex(r"\frac{\pi}{2}", font_size=20).next_to(time_axes.c2p(PI/2, 0), DOWN, buff=0.1),
            MathTex(r"\pi", font_size=20).next_to(time_axes.c2p(PI, 0), DOWN, buff=0.1),
            MathTex(r"\frac{3\pi}{2}", font_size=20).next_to(time_axes.c2p(3*PI/2, 0), DOWN, buff=0.1),
            MathTex(r"2\pi", font_size=20).next_to(time_axes.c2p(2*PI, 0), DOWN, buff=0.1)
        )
        
        def get_sine_wave(phase_shift, color):
            return ParametricFunction(
                lambda t: time_axes.c2p(t, np.sin(t + phase_shift)),
                t_range=[0, 2*PI], color=color
            )
        
        phase_a = get_sine_wave(0, RED)
        phase_b = get_sine_wave(-2*PI/3, GREEN)
        phase_c = get_sine_wave(-4*PI/3, BLUE)
        
        phase_labels = VGroup(
            Tex(r"\text{Phase A}", font_size=24, color=RED).to_edge(LEFT).shift(UP),
            Tex(r"\text{Phase B}", font_size=24, color=GREEN).to_edge(LEFT),
            Tex(r"\text{Phase C}", font_size=24, color=BLUE).to_edge(LEFT).shift(DOWN)
        )
        
        self.play(Write(three_phase_title), Write(three_phase_subtitle))
        self.play(Create(time_axes), FadeIn(time_labels), FadeIn(x_labels))
        
        self.play(Create(phase_a), FadeIn(phase_labels[0]))
        self.wait(0.5)
        self.play(Create(phase_b), FadeIn(phase_labels[1]))
        self.wait(0.5)
        self.play(Create(phase_c), FadeIn(phase_labels[2]))
        self.wait(1)
        
        dot_a = Dot(color=RED).move_to(time_axes.c2p(0, 0))
        dot_b = Dot(color=GREEN).move_to(time_axes.c2p(0, np.sin(-2*PI/3)))
        dot_c = Dot(color=BLUE).move_to(time_axes.c2p(0, np.sin(-4*PI/3)))
        
        self.play(FadeIn(dot_a), FadeIn(dot_b), FadeIn(dot_c))
        self.play(
            MoveAlongPath(dot_a, phase_a),
            MoveAlongPath(dot_b, phase_b),
            MoveAlongPath(dot_c, phase_c),
            run_time=4, rate_func=linear
        )
        self.wait(1)
        
        self.play(
            FadeOut(time_axes), FadeOut(time_labels), FadeOut(x_labels),
            FadeOut(phase_a), FadeOut(phase_b), FadeOut(phase_c),
            FadeOut(dot_a), FadeOut(dot_b), FadeOut(dot_c),
            FadeOut(phase_labels)
        )
        
        vector_subtitle = Tex(r"\text{Vector Representation}", font_size=32).next_to(three_phase_title, DOWN)
        self.play(ReplacementTransform(three_phase_subtitle, vector_subtitle))
        
        vector_axes = Axes(
            x_range=[-2.5, 2.5], y_range=[-2.5, 2.5],
            x_length=6, y_length=6, axis_config={"color": GRAY}
        ).add_coordinates()
        
        circle = Circle(radius=2, color=WHITE, stroke_width=1).move_to(vector_axes.get_origin())
        
        angle_tracker = ValueTracker(0)
        
        def get_vector(angle, color):
            return always_redraw(lambda: Arrow(
                vector_axes.get_origin(),
                vector_axes.c2p(2*np.cos(angle_tracker.get_value() + angle), 
                                2*np.sin(angle_tracker.get_value() + angle)),
                buff=0, color=color, stroke_width=3
            ))
        
        vecA = get_vector(0, RED)
        vecB = get_vector(-2*PI/3, GREEN)
        vecC = get_vector(-4*PI/3, BLUE)
        
        labels = VGroup(
            always_redraw(lambda: Tex(r"A", color=RED, font_size=24).next_to(vecA.get_end(), RIGHT, buff=0.1)),
            always_redraw(lambda: Tex(r"B", color=GREEN, font_size=24).next_to(vecB.get_end(), LEFT, buff=0.1)),
            always_redraw(lambda: Tex(r"C", color=BLUE, font_size=24).next_to(vecC.get_end(), DOWN, buff=0.1)),
        )
        
        angle_arc_AB = always_redraw(lambda: Arc(
            radius=0.5, angle=2*PI/3, start_angle=angle_tracker.get_value(), color=YELLOW
        ))
        angle_arc_BC = always_redraw(lambda: Arc(
            radius=0.7, angle=2*PI/3, start_angle=angle_tracker.get_value() - 2*PI/3, color=YELLOW
        ))
        
        angle_labels = VGroup(
            always_redraw(lambda: MathTex(r"120^\circ", font_size=24, color=YELLOW).move_to(
                0.9 * np.array([np.cos(angle_tracker.get_value() + PI/3), np.sin(angle_tracker.get_value() + PI/3), 0])
            )),
            always_redraw(lambda: MathTex(r"120^\circ", font_size=24, color=YELLOW).move_to(
                1.1 * np.array([np.cos(angle_tracker.get_value() - PI/3), np.sin(angle_tracker.get_value() - PI/3), 0])
            ))
        )
        
        self.play(Create(vector_axes), Create(circle))
        self.play(GrowArrow(vecA), Write(labels[0]))
        self.play(GrowArrow(vecB), Write(labels[1]))
        self.play(GrowArrow(vecC), Write(labels[2]))
        self.play(Create(angle_arc_AB), Create(angle_arc_BC), Write(angle_labels))
        
        self.play(angle_tracker.animate.set_value(2*PI), run_time=6, rate_func=linear)
        self.wait(1)
        
        problem_text = Tex(
            r"\text{Problem: Controlling three interdependent, time-varying quantities is complex!}",
            font_size=28, color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(problem_text))
        self.wait(2)
        
        self.play(
            FadeOut(three_phase_title), FadeOut(vector_subtitle),
            FadeOut(vector_axes), FadeOut(circle), 
            FadeOut(vecA), FadeOut(vecB), FadeOut(vecC),
            FadeOut(labels), FadeOut(angle_arc_AB), FadeOut(angle_arc_BC),
            FadeOut(angle_labels), FadeOut(problem_text)
        )
        
        # ------------------- 3. Clarke Transform -------------------
        clarke_title = Tex(r"\textbf{Clarke Transform ($\alpha\beta$ Transform)}", font_size=48, color=BLUE).to_edge(UP)
        clarke_subtitle = Tex(r"\text{Converting three-phase to two-phase stationary reference frame}", font_size=28).next_to(clarke_title, DOWN)
        
        self.play(Write(clarke_title), Write(clarke_subtitle))
        
        clarke_eq = MathTex(
            r"\begin{bmatrix} i_\alpha \\ i_\beta \end{bmatrix} = ",
            r"\frac{2}{3}",
            r"\begin{bmatrix} 1 & -\frac{1}{2} & -\frac{1}{2} \\ 0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2} \end{bmatrix}",
            r"\begin{bmatrix} i_a \\ i_b \\ i_c \end{bmatrix}",
            font_size=36
        ).shift(UP * 1.5)
        
        self.play(Write(clarke_eq), run_time=2)
        self.wait(1)
        
        clarke_axes = Axes(
            x_range=[-2.5, 2.5], y_range=[-2.5, 2.5],
            x_length=6, y_length=6, axis_config={"color": GRAY}
        ).shift(DOWN * 1.5)
        
        clarke_labels = VGroup(
            MathTex(r"\alpha", font_size=24).next_to(clarke_axes.x_axis.get_end(), RIGHT),
            MathTex(r"\beta", font_size=24).next_to(clarke_axes.y_axis.get_end(), UP)
        )
        
        angle_tracker.set_value(0)
        
        vecA = always_redraw(lambda: Arrow(
            clarke_axes.get_origin(),
            clarke_axes.c2p(2*np.cos(angle_tracker.get_value()), 0),
            buff=0, color=RED, stroke_width=3
        ))
        vecB = always_redraw(lambda: Arrow(
            clarke_axes.get_origin(),
            clarke_axes.c2p(
                2*np.cos(angle_tracker.get_value() - 2*PI/3),
                2*np.sin(angle_tracker.get_value() - 2*PI/3)
            ),
            buff=0, color=GREEN, stroke_width=3
        ))
        vecC = always_redraw(lambda: Arrow(
            clarke_axes.get_origin(),
            clarke_axes.c2p(
                2*np.cos(angle_tracker.get_value() - 4*PI/3),
                2*np.sin(angle_tracker.get_value() - 4*PI/3)
            ),
            buff=0, color=BLUE, stroke_width=3
        ))
        
        vec_alpha_beta = always_redraw(lambda: Arrow(
            clarke_axes.get_origin(),
            clarke_axes.c2p(
                2*np.cos(angle_tracker.get_value()),
                2*np.sin(angle_tracker.get_value())
            ),
            buff=0, color=YELLOW, stroke_width=5
        ))
        
        alpha_beta_label = always_redraw(lambda: MathTex(r"\alpha\beta", font_size=24, color=YELLOW).next_to(
            vec_alpha_beta.get_end(), UP+RIGHT, buff=0.1
        ))
        
        circle = Circle(radius=2, color=WHITE, stroke_width=1).move_to(clarke_axes.get_origin())
        
        self.play(Create(clarke_axes), Write(clarke_labels))
        self.play(Create(circle))
        self.play(GrowArrow(vecA), GrowArrow(vecB), GrowArrow(vecC))
        self.play(GrowArrow(vec_alpha_beta), Write(alpha_beta_label))
        
        self.play(angle_tracker.animate.set_value(2*PI), run_time=6, rate_func=linear)
        self.wait(1)
        
        clarke_explanation = Tex(
            r"\text{We've reduced three variables to two, but they still vary with time!}",
            font_size=28, color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(clarke_explanation))
        self.wait(2)
        
        self.play(
            FadeOut(clarke_title), FadeOut(clarke_subtitle), FadeOut(clarke_eq),
            FadeOut(clarke_axes), FadeOut(clarke_labels), FadeOut(circle),
            FadeOut(vecA), FadeOut(vecB), FadeOut(vecC),
            FadeOut(vec_alpha_beta), FadeOut(alpha_beta_label),
            FadeOut(clarke_explanation)
        )
        
        # ------------------- 4. Park Transform -------------------
        park_title = Tex(r"\textbf{Park Transform ($dq$ Transform)}", font_size=48, color=BLUE).to_edge(UP)
        park_subtitle = Tex(r"\text{Converting to a rotating reference frame}", font_size=32).next_to(park_title, DOWN)
        
        self.play(Write(park_title), Write(park_subtitle))
        
        park_eq = MathTex(
            r"\begin{bmatrix} i_d \\ i_q \end{bmatrix} =",
            r"\begin{bmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{bmatrix}",
            r"\begin{bmatrix} i_\alpha \\ i_\beta \end{bmatrix}",
            font_size=36
        ).shift(UP * 2)
        
        park_explanation = Tex(
            r"\text{This is a rotation matrix that aligns with the rotating field!}",
            font_size=28, color=YELLOW
        ).next_to(park_eq, DOWN, buff=0.5)
        
        self.play(Write(park_eq), run_time=2)
        self.play(Write(park_explanation))
        self.wait(2)
        
        self.play(FadeOut(park_eq), FadeOut(park_explanation))
        
        park_axes = Axes(
            x_range=[-2.5, 2.5], y_range=[-2.5, 2.5],
            x_length=6, y_length=6, axis_config={"color": GRAY}
        ).shift(DOWN * 1.5)
        
        alpha_beta_labels = VGroup(
            MathTex(r"\alpha", font_size=24, color=WHITE).next_to(park_axes.x_axis.get_end(), RIGHT),
            MathTex(r"\beta", font_size=24, color=WHITE).next_to(park_axes.y_axis.get_end(), UP)
        )
        
        angle_tracker.set_value(0)
        
        dq_axes = VGroup(
            always_redraw(lambda: Line(
                park_axes.get_origin(),
                park_axes.c2p(2.5*np.cos(angle_tracker.get_value()), 2.5*np.sin(angle_tracker.get_value())),
                color=YELLOW, stroke_width=2
            )),
            always_redraw(lambda: Line(
                park_axes.get_origin(),
                park_axes.c2p(
                    2.5*np.cos(angle_tracker.get_value() + PI/2),
                    2.5*np.sin(angle_tracker.get_value() + PI/2)
                ),
                color=YELLOW, stroke_width=2
            ))
        )
        
        dq_labels = VGroup(
            always_redraw(lambda: Tex(r"d", font_size=24, color=YELLOW).next_to(
                dq_axes[0].get_end(), RIGHT if np.cos(angle_tracker.get_value()) > 0 else LEFT, buff=0.1
            )),
            always_redraw(lambda: Tex(r"q", font_size=24, color=YELLOW).next_to(
                dq_axes[1].get_end(), UP if np.sin(angle_tracker.get_value() + PI/2) > 0 else DOWN, buff=0.1
            ))
        )

        circle = Circle(radius=2, color=WHITE, stroke_width=1).move_to(park_axes.get_origin())
        alpha_beta_vector = Arrow(
            park_axes.get_origin(), park_axes.c2p(2, 0),
            buff=0, color=GREEN, stroke_width=4
        )
        
        dq_vector = always_redraw(lambda: Arrow(
            park_axes.get_origin(),
            park_axes.c2p(
                2*np.cos(-angle_tracker.get_value()),
                2*np.sin(-angle_tracker.get_value())
            ),
            buff=0, color=RED, stroke_width=4
        ))
        
        angle_arc = always_redraw(lambda: Arc(
            radius=0.5, angle=angle_tracker.get_value(), start_angle=0, color=YELLOW
        ))
        
        angle_label = always_redraw(lambda: MathTex(
            r"\theta", font_size=24, color=YELLOW
        ).next_to(
            angle_arc, RIGHT if angle_tracker.get_value() < PI else LEFT, buff=0.1
        ))
        
        frame_labels = VGroup(
            VGroup(
                Text("Stationary ", font_size=24, color=GREEN),
                MathTex(r"\alpha\beta", font_size=24, color=GREEN),
                Text(" frame", font_size=24, color=GREEN)
            ).arrange(RIGHT, buff=0).to_edge(UP, buff=2).to_edge(LEFT),
            VGroup(
                Text("Rotating ", font_size=24, color=YELLOW),
                MathTex(r"dq", font_size=24, color=YELLOW),
                Text(" frame", font_size=24, color=YELLOW)
            ).arrange(RIGHT, buff=0).to_edge(UP, buff=2).to_edge(RIGHT)
        )
        
        self.play(Create(park_axes), Write(alpha_beta_labels))
        self.play(Create(circle))
        self.play(GrowArrow(alpha_beta_vector))
        self.play(Create(dq_axes), Write(dq_labels))
        self.play(GrowArrow(dq_vector))
        self.play(Create(angle_arc), Write(angle_label))
        self.play(Write(frame_labels))
        
        self.play(angle_tracker.animate.set_value(2*PI), run_time=8, rate_func=linear)
        self.wait(1)
        
        park_result = Tex(
            r"\text{The }dq\text{ vector is now constant in the rotating reference frame!}",
            font_size=28, color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(park_result))
        self.wait(2)
        
        control_benefit = Tex(
            r"\text{This makes control easier --- we can use DC control techniques!}",
            font_size=28, color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        
        self.play(ReplacementTransform(park_result, control_benefit))
        self.wait(2)
        
        self.play(
            FadeOut(park_title), FadeOut(park_subtitle),
            FadeOut(park_axes), FadeOut(alpha_beta_labels), FadeOut(circle),
            FadeOut(alpha_beta_vector), FadeOut(dq_vector),
            FadeOut(dq_axes), FadeOut(dq_labels),
            FadeOut(angle_arc), FadeOut(angle_label),
            FadeOut(frame_labels), FadeOut(control_benefit)
        )
        
        # ------------------- 5. Applications -------------------
        applications_title = Tex(r"\textbf{Applications of Park Transform}", font_size=48, color=BLUE).to_edge(UP)
        self.play(Write(applications_title))
        
        applications = VGroup(
            VGroup(
                Tex(r"$\bullet$ \text{Field-Oriented Control (FOC)}", font_size=32, color=WHITE),
                Tex(r"\text{Precise torque control in AC motors}", font_size=28, color=GRAY)
            ).arrange(RIGHT, buff=0.5),
            VGroup(
                Tex(r"$\bullet$ \text{Direct Torque Control (DTC)}", font_size=32, color=WHITE),
                Tex(r"\text{Fast dynamic response in drives}", font_size=28, color=GRAY)
            ).arrange(RIGHT, buff=0.5),
            VGroup(
                Tex(r"$\bullet$ \text{Grid-Connected Inverters}", font_size=32, color=WHITE),
                Tex(r"\text{Synchronization with grid voltage}", font_size=28, color=GRAY)
            ).arrange(RIGHT, buff=0.5),
            VGroup(
                Tex(r"$\bullet$ \text{Power Quality Analysis}", font_size=32, color=WHITE),
                Tex(r"\text{Harmonic detection and compensation}", font_size=28, color=GRAY)
            ).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(applications_title, DOWN, buff=0.8)
        
        for app in applications:
            self.play(Write(app), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        self.play(FadeOut(applications_title), FadeOut(applications))
        
        # ---------------------- 6. Conclusion ----------------------
        conclusion_title = Tex(r"\textbf{Key Takeaways}", font_size=48, color=BLUE).to_edge(UP)
        self.play(Write(conclusion_title))
        
        conclusion = VGroup(
            VGroup(
                Tex(r"1.", font_size=32, color=YELLOW),
                Tex(r"\text{Park Transform converts time-varying AC to DC-like values}", font_size=32)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Tex(r"2.", font_size=32, color=YELLOW),
                Tex(r"\text{Enables simpler control with DC techniques}", font_size=32)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Tex(r"3.", font_size=32, color=YELLOW),
                Tex(r"\text{Essential for modern motor drives and converters}", font_size=32)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Tex(r"4.", font_size=32, color=YELLOW),
                Tex(r"\text{Geometric intuition aids understanding}", font_size=32)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(conclusion_title, DOWN, buff=0.8)
        
        for point in conclusion:
            self.play(Write(point), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        
        thanks = Tex(r"\text{Thank You for Watching!}", font_size=48, color=YELLOW).next_to(conclusion, DOWN, buff=1)
        self.play(Write(thanks))
        self.wait(3)
        self.play(FadeOut(conclusion_title), FadeOut(conclusion), FadeOut(thanks))
        
        # Final cleanup
        self.clear()