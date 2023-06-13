from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.middleware.csrf import get_token
import random


def homepage_view(request):
    csrf_token = get_token(request)
    return render(request, 'home.html', {'csrf_token': csrf_token})

def description(request):
    return render(request, 'description.html')


class CalculateAreaView(View):
    template_name = 'shape_drawer.html'
    canvas_width_pixels = 400  # Width of the canvas in pixels
    canvas_height_pixels = 400  # Height of the canvas in pixels
    canvas_width_meters = 5  # Width of the canvas in meters
    canvas_height_meters = 5  # Height of the canvas in meters
    tolerance = 5  # Tolerance value for checking if shape is closed

    def post(self, request):
        points = list(request.POST.getlist('points[]'))

        if len(points) < 3:
            error_message = 'Vähemalt 3 punkti on vaja, et arvutada pindala'
            return JsonResponse({'error': error_message})

        if not self.is_shape_closed(points):
            error_message = 'Palun joonistage korrektne kuju'
            return JsonResponse({'error': error_message})

        try:
            result = self.calculate_area(points)
            estimated_area = result['estimated_area']
            points_inside = result['points_inside']
            canvas_area = result['canvas_area']
            return JsonResponse({'estimated_area': estimated_area})
        except ValueError as e:
            error_message = str(e)
            return JsonResponse({'error': error_message})

    def is_shape_closed(self, points):
        first_point = tuple(map(float, str(points[0]).strip()[1:-1].split(',')))
        last_point = tuple(map(float, str(points[-1]).strip()[1:-1].split(',')))

        # Compare the coordinates of the first and last points within tolerance
        if abs(first_point[0] - last_point[0]) > self.tolerance or abs(first_point[1] - last_point[1]) > self.tolerance:
            return False

        return True

    def is_point_inside_shape(self, x, y, points):
        num_intersections = 0

        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]

            if (y1 < y and y2 >= y) or (y1 >= y and y2 < y):
                if x1 + (y - y1) / (y2 - y1) * (x2 - x1) > x:
                    num_intersections += 1

        return num_intersections % 2 == 1

    def calculate_area(self, points):
        if len(points) < 3:
            raise ValueError('Vähemalt 3 punkti on vaja, et arvutada pindala')

        # Convert the received points to a list of tuples
        points = [tuple(map(float, str(point).split(','))) for point in points]

        # Check if the shape is closed
        if not self.is_shape_closed(points):
            raise ValueError('Please draw a valid shape')

        # Find the minimum and maximum x and y coordinates
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)

        # Generate random points within the bounding box of the shape
        num_points = 10000  # Number of random points to generate
        points_inside = 0

        for _ in range(num_points):
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)

            if self.is_point_inside_shape(x, y, points):
                points_inside += 1

        # Calculate the scaling factors based on the actual canvas size in pixels and meters
        x_scale_factor = self.canvas_width_meters / self.canvas_width_pixels
        y_scale_factor = self.canvas_height_meters / self.canvas_height_pixels

        # Scale the estimated area based on the canvas size and convert to square meters
        estimated_area_pixels = (points_inside / num_points) * (max_x - min_x) * (max_y - min_y)
        estimated_area_meters = estimated_area_pixels * (x_scale_factor * y_scale_factor)

        result = {
            'estimated_area': estimated_area_meters,
            'points_inside': points_inside,
            'canvas_area': self.canvas_width_meters * self.canvas_height_meters,
        }

        return result
