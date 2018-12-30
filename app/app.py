import csv
from flask import Flask, render_template
import random
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

app = Flask(__name__)

@app.route('/')
def index():
    data = loadData()

    hover = create_hover_tool()
    plot = create_bar_chart(data, "Domestic Flights by Airline", "labels",
                            "data1", hover)
    script, div = components(plot)

    return render_template("chart.html",
                           the_div=div, the_script=script)


@app.route('/year/<int:year>')
def year(year):
	return 'This will display information for year %d' % year

def loadData():
	with open('../data-preprocess/Dec2017.txt') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		i = 0
		data = {}
		for row in csv_reader:
			print(i)
			if i == 0:
				data['labels'] = row
			elif i == 1:
				data['data1'] = [float(numeric_str)/1000000 for numeric_str in row]
				print(data['data1'])
			elif i == 2:
				data['data2'] = [float(numeric_str) for numeric_str in row]
			i = i + 1
		return data


def create_hover_tool():
    # we'll code this function in a moment
    return None


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=600):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)

    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.1)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  outline_line_color="#666666")

    plot.left[0].formatter.use_scientific = False

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Number of Passengers (Millions)"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "Airline"
    plot.xaxis.major_label_orientation = 1
    return plot