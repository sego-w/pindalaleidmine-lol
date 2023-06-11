from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import random


class ShapeDrawerView(View):
    template_name = 'shape_drawer.html'
    canvas_width_meters = 5  # Width of the canvas in meters
    canvas_height_meters = 5  # Height of the canvas in meters

    def get(self, request):
        print("Django app activated")
        return render(request, self.template_name)

    def post(self, request):
        print("Post method called")
        points = request.POST.getlist('points[]')

        if len(points) < 3:
            error_message = 'At least 3 points are required to calculate the area'
            return JsonResponse({'error': error_message})

        result = self.calculate_area(points)

        estimated_area = result['estimated_area']
        points_inside = result['points_inside']
        canvas_area = result['canvas_area']

        print("Points Inside:", points_inside)
        print("Canvas Area:", canvas_area)
        print("Estimated Area:", estimated_area)

        return JsonResponse({'estimated_area': estimated_area})

    def calculate_area(self, points):
        if len(points) < 3:
            return {'error': 'At least 3 points are required to calculate the area'}

        # Convert the received points to a list of tuples
        points = [tuple(map(float, point.split(','))) for point in points]

        # Find the minimum and maximum x and y coordinates
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)

        # Generate random points within the bounding box of the shape
        num_points = 100000  # Number of random points to generate
        points_inside = 0

        for _ in range(num_points):
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)

            if self.is_point_inside_shape(x, y, points):
                points_inside += 1

        # Calculate the scaling factors
        canvas_width_pixels = max_x - min_x
        canvas_height_pixels = max_y - min_y
        x_scale_factor = self.canvas_width_meters / canvas_width_pixels
        y_scale_factor = self.canvas_height_meters / canvas_height_pixels

        # Scale the canvas area
        canvas_area = self.canvas_width_meters * self.canvas_height_meters

        # Scale the estimated area
        estimated_area = (points_inside / num_points) * canvas_area

        result = {
            'estimated_area': estimated_area,
            'points_inside': points_inside,
            'canvas_area': canvas_area,
        }

        return result

    def is_point_inside_shape(self, x, y, points):
        # Implement the Winding Number algorithm to check if a point is inside a shape
        wn = 0  # Winding number

        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]

            if y1 <= y:
                if y2 > y and self.is_left(x1, y1, x2, y2, x, y) > 0:
                    wn += 1
            else:
                if y2 <= y and self.is_left(x1, y1, x2, y2, x, y) < 0:
                    wn -= 1

        return wn != 0

    def is_left(self, x1, y1, x2, y2, x, y):
        return (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1)
