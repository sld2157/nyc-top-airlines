"""The main logic for the NYC Airports web application
"""

from bokeh.models import (HoverTool, Plot, Legend, LinearAxis, Grid, DataRange1d)
from bokeh.models.glyphs import Line
from bokeh.models.markers import Circle
from bokeh.palettes import viridis
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template
from operator import add
import random

#NYC-Airline imports
from GetAirlineData import (loadData, getColors)

app = Flask(__name__)

@app.route('/')
def index():
    data = loadData()
    colors = getColors(data)

    hover = create_hover_tool()
    plot = create_bar_chart(data, "Domestic Flights by Airline", hover, colors)
    script, div = components(plot)

    return render_template("chart.html",
                           the_div=div, the_script=script)


@app.route('/year/<int:year>')
def year(year):
	return 'This will display information for year %d' % year


def create_hover_tool():
    # we'll code this function in a moment
    return None


def create_bar_chart(data, title, hover_tool, colors):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """

    xdr = DataRange1d()
    ydr = DataRange1d()

    tools = ["tap"]
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=1200,
                  plot_height=800, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  outline_line_color="#666666", x_axis_type='datetime')

    plot.left[0].formatter.use_scientific = False

    legendItems = []

    for airline in data:
    	plotLineAndPoints(data[airline]['date'], data[airline]['domestic'], 'dashed', 5, colors[airline], plot, airline, legendItems)
    	plotLineAndPoints(data[airline]['date'], data[airline]['international'], 'dotted', 5, colors[airline], plot, airline, legendItems)

    	total = list(map(add, data[airline]['domestic'], data[airline]['international']))

    	plotLineAndPoints(data[airline]['date'], total, 'solid', 8, colors[airline], plot, airline, legendItems)
    	
    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.ygrid.grid_line_alpha = 0.1

    #Style Y axis
    plot.yaxis.axis_label = "Number of Passengers (Millions)"
    plot.yaxis.axis_label_text_font_size = '12pt'
    plot.yaxis.axis_label_text_font_style = 'normal'

    #Style X axis
    plot.xaxis.axis_label = "Airline"
    plot.xaxis.major_label_orientation = 1
    plot.xaxis.axis_label_text_font_size = '12pt'
    plot.xaxis.axis_label_text_font_style = 'normal'
    plot.xaxis[0].formatter.days = '%b %Y'

    #Create legend
    legend = Legend(items=legendItems, location=(0,-30))
    plot.add_layout(legend, 'right')

    return plot

def plotLineAndPoints(X, Y, lineStyle, pointSize, color, plot, airline, legendItems):
	plot.line(x=X, y=Y, line_color=color, line_width=2, line_alpha=0.6, line_dash=lineStyle)

	circle_renderer = plot.circle(x=X, y=Y, size=pointSize, fill_color=color, line_color=color)
	circle_renderer.selection_glyph = Circle(fill_color='black', line_color='black')
	circle_renderer.nonselection_glyph = Circle(fill_color=color, line_color=color)

	if lineStyle == 'solid':
		legendItems.append((airline, [circle_renderer]))

