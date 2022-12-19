# TreeLights
Here is (most of) the Python code I used to map and animate 500 LEDs on my tree. The whole project is inspired by Matt Parker from Stand-up Maths on YouTube, so watch these if you haven't already:

- Stand-up Maths: [I wired my tree with 500 LED lights and calculated their 3D coordinates.](https://www.youtube.com/watch?v=TvlpIojusBE) 
- Stand-up Maths: [Stand-up Maths: My 500-LED xmas tree got into Harvard.](https://www.youtube.com/watch?v=WuMRJf6B5Q4)

I used a WS2811 LED strip connected to a Raspberry Pi Zero W, and a host computer with a webcam to capture, process and simulate the LEDs.

1. `capture.py` talks to the Pi Zero to individually light each LED and take a picture.
2. `process.py` performs some basic image processing and curve fitting to calculate the coordinates of each LED.
3. `simulate.py` visually simulates animation programs.

Each file (hopefully) has further explanations inside. Have fun.

## Dependencies
- Python 3.10.8
- [NumPy](https://numpy.org/) 1.24.0
- [SciPy](https://scipy.org/) 1.9.3
- [Matplotlib](https://matplotlib.org/) 3.6.2
- [OpenCV on Wheels](https://pypi.org/project/opencv-python/) 4.6.0.66

Dependencies can be installed using: `pip install -r requirements.txt`

Earlier versions may also be compatible.

## Licensing
This program is free software: you can redistribute it and/or modify it under the terms of the [GNU General Public License](http://www.gnu.org/licenses/gpl-3.0.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.