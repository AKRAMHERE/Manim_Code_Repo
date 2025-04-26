from manim import *
import numpy as np

class EVCharacteristicsEnhanced(Scene):
    def construct(self):
        # Title sequence with animated motor
        title = Text("Electric Vehicle Motor Characteristics", font_size=40)
        title.to_edge(UP)
        
        # Create animated motor icon
        motor = VGroup()
        circle = Circle(radius=0.5, color=BLUE)
        rotor = Line(start=circle.get_center(), end=circle.get_right(), color=WHITE)
        motor.add(circle, rotor)
        motor.next_to(title, LEFT)
        
        # Animate motor rotation
        self.play(Write(title))
        self.play(Create(motor))
        self.play(Rotate(rotor, angle=TAU*2, about_point=circle.get_center()), run_time=2)
        self.wait(1)

        # Operating regions diagram
        operating_regions = self.create_operating_regions()
        self.play(FadeOut(motor), operating_regions.animate.to_edge(UP))
        self.wait(2)

        # Interactive torque-speed curve
        self.show_interactive_torque_speed()
        self.wait(2)

        # Dynamic power calculation
        self.show_power_calculation()
        self.wait(2)

        # Back EMF animation
        self.show_back_emf()
        self.wait(2)

        # Efficiency map
        self.show_efficiency_map()
        self.wait(2)

    def create_operating_regions(self):
        # Create operating regions diagram
        regions = VGroup()
        
        # Constant torque region
        rect1 = Rectangle(width=3, height=4, color=BLUE)
        label1 = Text("Constant\nTorque\nRegion", font_size=20).move_to(rect1)
        region1 = VGroup(rect1, label1)
        
        # Constant power region
        rect2 = Rectangle(width=3, height=4, color=RED)
        label2 = Text("Constant\nPower\nRegion", font_size=20).move_to(rect2)
        region2 = VGroup(rect2, label2)
        region2.next_to(region1, RIGHT, buff=0)
        
        regions.add(region1, region2)
        return regions

    def show_interactive_torque_speed(self):
        # Create axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True},
        ).add_coordinates()
        
        labels = axes.get_axis_labels(
            x_label="Speed (RPM × 1000)",
            y_label="Torque (Nm)"
        )

        # Create dot that moves along torque curve
        def torque_func(x):
            return 8 * np.exp(-0.2 * x)
        
        curve = axes.plot(torque_func, color=BLUE)
        dot = Dot(color=YELLOW)
        dot.move_to(axes.c2p(0, torque_func(0)))
        
        # Value trackers for animation
        x_tracker = ValueTracker(0)
        
        # Update dot position
        dot.add_updater(
            lambda d: d.move_to(
                axes.c2p(
                    x_tracker.get_value(),
                    torque_func(x_tracker.get_value())
                )
            )
        )

        self.play(Create(axes), Write(labels))
        self.play(Create(curve), Create(dot))
        self.play(x_tracker.animate.set_value(10), run_time=3)
        self.wait()

    def show_power_calculation(self):
        # Create power calculation visualization
        formula = MathTex("P = T x w")
        
        # Create dynamic values
        torque_value = DecimalNumber(8, num_decimal_places=1)
        speed_value = DecimalNumber(0, num_decimal_places=1)
        power_value = DecimalNumber(0, num_decimal_places=1)
        
        calc_group = VGroup(
            Text("Torque: "), torque_value, Text(" Nm"),
            Text("\nSpeed: "), speed_value, Text(" rad/s"),
            Text("\nPower: "), power_value, Text(" kW")
        ).arrange(RIGHT)
        
        calc_group.next_to(formula, DOWN)
        
        # Update values
        speed_tracker = ValueTracker(0)
        
        def update_power(value):
            torque = 8 * np.exp(-0.2 * speed_tracker.get_value())
            power = torque * speed_tracker.get_value()
            value.set_value(power)
            
        power_value.add_updater(update_power)
        
        self.play(Write(formula), Create(calc_group))
        self.play(speed_tracker.animate.set_value(10), run_time=3)
        self.wait()

    def show_back_emf(self):
        # Create back EMF visualization
        emf_title = Text("Back EMF Generation", font_size=30)
        
        # Create simplified motor diagram
        motor = Circle(radius=1)
        magnet_N = Text("N", color=RED)
        magnet_S = Text("S", color=BLUE)
        
        magnet_N.move_to(motor.point_at_angle(0))
        magnet_S.move_to(motor.point_at_angle(PI))
        
        conductor = Line(
            start=motor.point_at_angle(PI/2),
            end=motor.point_at_angle(3*PI/2),
            color=YELLOW
        )
        
        motor_group = VGroup(motor, magnet_N, magnet_S, conductor)
        
        # Create voltage indicator
        voltage_meter = Rectangle(width=2, height=1)
        voltage_value = DecimalNumber(0, num_decimal_places=1)
        voltage_value.move_to(voltage_meter)
        
        meter_group = VGroup(voltage_meter, voltage_value)
        meter_group.next_to(motor_group, RIGHT)
        
        # Animation
        self.play(Create(motor_group), Create(meter_group))
        
        # Rotate motor and update voltage
        self.play(
            Rotate(conductor, angle=TAU*2, about_point=motor.get_center()),
            voltage_value.animate.set_value(10),
            run_time=3
        )
        self.wait()

    def show_efficiency_map(self):
        # Create efficiency map using color mesh
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=4,
        ).add_coordinates()
        
        labels = axes.get_axis_labels(
            x_label="Speed (RPM x 1000)",
            y_label="Torque (Nm)"
        )
        
        # Create efficiency regions using color gradient
        efficiency_regions = []
        colors = [BLUE, GREEN, YELLOW, RED]
        
        for i in range(4):
            region = Rectangle(
                width=1.5,
                height=1,
                fill_opacity=0.5,
                color=colors[i]
            )
            region.move_to(axes.c2p(2+2*i, 5))
            efficiency_regions.append(region)
        
        # Add legend
        legend = VGroup()
        for i, (color, text) in enumerate(zip(
            colors,
            ["70%", "80%", "90%", "95%"]
        )):
            rect = Rectangle(width=0.3, height=0.3, fill_opacity=0.5, color=color)
            label = Text(text, font_size=20)
            label.next_to(rect, RIGHT)
            group = VGroup(rect, label)
            group.next_to(axes, RIGHT, buff=0.5)
            if i > 0:
                group.next_to(legend[-1], DOWN)
            legend.add(group)
        
        self.play(Create(axes), Write(labels))
        self.play(*[Create(region) for region in efficiency_regions])
        self.play(Create(legend))
        self.wait()

if __name__ == "__main__":
    from manim import *
    config.frame_width = 16
    config.frame_height = 9
    config.pixel_width = 1920
    config.pixel_height = 1080
    with tempconfig({"quality": "production_quality", "preview": True}):
        scene = EVCharacteristicsEnhanced()
        scene.render()