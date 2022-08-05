from manim import *
import numpy as np
from numpy import cos, sin

Blue = "#28CDD7"
Red = "#D73228"

class Complex_Cos(Scene):
    def construct(self):
        angle_tracker = ValueTracker(0)
        angle = angle_tracker.get_value()
        
        # 1 means red line = blue line
        # -1 means the red line = blue line mirrored along the x axis
        mirror_tracker = ValueTracker(1)
        
        # 0 means the red line come out of the origin
        # 1 means the red line is translated to come out of the tip of the blue line
        trans_tracker = ValueTracker(0)
        
        plane = ComplexPlane()
        plane.height *= 1.5
        plane.add_coordinates()
        
        def terminal(a):
            return plane.c2p(cos(a), sin(a))
        
        # creating and setting up the cosine formula
        cos_formula = MathTex(r"\cos(\theta) = \frac{e^{i\theta} + e^{-i\theta}}{2}")
        cos_formula.move_to(plane.c2p(-3.25,2.25))
        background_rectangle = BackgroundRectangle(cos_formula)
        
        # splitting up the cosine formula into multiple variables
        cos_t_equals = cos_formula[0][:7]
        e_it = cos_formula[0][7:10]
        plus = cos_formula[0][10]
        e_neg_it = cos_formula[0][11:15]
        over_two = cos_formula[0][15:17]
        
        e_it.set_color(Blue)
        e_neg_it.set_color(Red)
        
        origin = plane.c2p(0,0)
        
        # creating a yellow circle
        circle = plane.plot_parametric_curve(
            lambda t: np.array(
                    [np.cos(t),
                     np.sin(t)]),
            t_range = [0, angle],
            color = YELLOW,
            stroke_width = 2)
        
        # creating the blue line and the red line, then making a group of both
        radius = Line(start=origin, end=terminal(angle), color=Blue)
        neg_radius = Line(start=origin, end=terminal(1), color=Red)
        radii = VGroup(radius, neg_radius)
        
        dashed_line = plane.get_vertical_line(terminal(0.5))
        
        #draws the circle in sync with the value of angle_tracker
        def circle_updater(mobject):
            angle = angle_tracker.get_value()
            # no need to update the circle if it is fully drawn (but it is safer to include some buffer)
            if angle <= TAU+1:
                mobject.become(
                    plane.plot_parametric_curve(
                        lambda t: np.array(
                                [np.cos(t),
                                 np.sin(t)]),
                        # t_range is the only thing that changes
                        t_range = [0, angle],
                        color = mobject.get_color(),
                        stroke_width = mobject.get_stroke_width()
                    )
                )
        
        # rotates the blue line in sync with the value of angle_tracker
        def radius_updater(mobject):
            angle = angle_tracker.get_value()
            mobject.put_start_and_end_on(origin, terminal(angle))
        
        # controls the red line based on the angle and the values of flip and trans
        def neg_radius_updater(mobject):
            principal_angle = angle_tracker.get_value() - TAU
            mirror = mirror_tracker.get_value()
            trans = trans_tracker.get_value()
            # no need to update the line if it hasn't been added yet
            if principal_angle >= 1:
                # if trans == 0, then the line goes from the origin until the terminal point
                # if trans == 1, then the starting and ending point are translated
                #                so that the red line extends from the blue line
                new_start = origin + trans*terminal(principal_angle)
                new_end = terminal(mirror*principal_angle) + trans*terminal(principal_angle)
                mobject.put_start_and_end_on(new_start, new_end)
            
            
        circle.add_updater(circle_updater)
        radius.add_updater(radius_updater)
        neg_radius.add_updater(neg_radius_updater)
        
        self.add(plane, circle, radius, background_rectangle, cos_t_equals)
        
        self.wait(0.25)
        self.play(angle_tracker.animate.set_value(TAU+1), run_time=1)
        self.add(neg_radius)
        self.bring_to_back(neg_radius)
        self.bring_to_back(circle)
        self.bring_to_back(plane)
        self.wait(0.5)
        
        self.play(Indicate(radius), run_time=1.5)
        self.wait(0.5)
        self.play(Write(e_it), run_time=2)
        self.wait(0.5)
        
        self.play(mirror_tracker.animate.set_value(-1), run_time=2)
        self.wait(0.5)
        self.play(Indicate(neg_radius), run_time=1.5)
        self.wait(0.5)
        self.play(Write(e_neg_it), run_time=2)
        self.wait(0.5)
        
        self.play(trans_tracker.animate.set_value(1), run_time=2)
        self.wait(0.5)
        self.play(Indicate(radii), run_time=1.5)
        self.wait(0.5)
        self.play(Write(plus), run_time=2)
        self.wait()
        
        self.play(angle_tracker.animate.set_value(2*TAU+0.5), rate_func=rate_functions.ease_in_out_sine, run_time=5)
        
        self.wait()
        self.play(Create(dashed_line), run_time=1.5)
        self.wait(0.5)
        self.play(Write(over_two), run_time=2)
        self.wait()


# manim -pqp C:\Users\minde\Desktop\project\Tinkering.py Complex_Cos
# manim -pql C:\Users\minde\Desktop\project\Tinkering.py Complex_Cos
