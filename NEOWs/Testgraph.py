# Import Bokeh modules
from bokeh.plotting import figure, output_file, show
from bokeh.models import Label # Import Label class

# Define the data for the x and y axes
x = [1, 2, 3, 4, 5] # distance in km
y = [10, 20, 30, 40, 50] # speed in km/h

# Define the size of the circles
size = [10, 15, 20, 25, 30] # diameter in pixels

# Define the names of the circles
names = ["A", "B", "C", "D", "E"] # arbitrary names

# Create a figure object
p = figure(title="Scatter graph of distance vs speed", x_axis_label="Distance (km)", y_axis_label="Speed (km/h)")

# Add circle glyphs to the figure
p.circle(x, y, size=size, fill_color="blue", line_color="black")

# Create labels for each circle
for i in range(len(x)):
    label = Label(x=x[i], y=y[i], x_offset=10, y_offset=10, text=names[i])
    p.add_layout(label)

# Specify the output file name
output_file("scatter_graph_with_labels.html")

# Display the figure
show(p)