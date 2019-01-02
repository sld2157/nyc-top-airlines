"""The main logic for the NYC Airports web application
"""
from bokeh.layouts import (column, widgetbox)
from bokeh.models import (CustomJS, HoverTool, Legend, Plot, LinearAxis, Grid, DataRange1d)
from bokeh.models.annotations import Label
from bokeh.models.glyphs import Line
from bokeh.models.markers import Circle
from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.palettes import viridis
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from datetime import datetime
from flask import Flask, render_template
from operator import add
import random

#NYC-Airline imports
from GetAirlineData import (loadData, getColors)
from CategorialLegend import CategorialLegend

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

    xdr = DataRange1d(bounds='auto')
    ydr = DataRange1d(bounds='auto')

    hover = HoverTool(
        tooltips="""
            <div>
            	<p><span style="font-weight: bold;">%s</span> - %s</p>
				<p>%s million %s passengers</p>
			</div>
    	""" % ("@airline", "@date{%b %Y}", "$y", "$name"),
    	formatters={
    	'date': 'datetime'
    	},
    	names=['domestic', 'international', 'total']
    )

    tools = [hover, 'pan', 'box_zoom', 'zoom_in', 'zoom_out', 'wheel_zoom']

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=1200,
                  plot_height=800, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  outline_line_color="#666666", x_axis_type='datetime', border_fill_color='#DBECFC')

    plot.left[0].formatter.use_scientific = False

    legendItems = []

    for airline in data:

        color = colors[airline]
        source = ColumnDataSource(data = data[airline])
        legendItems.append(([airline, "Domestic"], 
        	(plot.line(x='date', y='domestic', line_color=color, line_width=2, line_alpha=0.6, line_dash='dashed', source=source))))
        legendItems.append(([airline, "Domestic"], 
        	plot.circle(x='date', y='domestic', size=5, fill_color=color, source=source, name='domestic', line_color=color)))
        legendItems[-1][1].hover_glyph = Circle(line_width=6, line_color=color, line_alpha=0.2, fill_color=color)


        
        source = ColumnDataSource(data = data[airline])
        legendItems.append(([airline, "Total"], 
            plot.line(x='date', y='total', line_color=color, line_width=2, line_alpha=0.6, source=source)))
        legendItems.append(([airline, "Total"],
            plot.circle(x='date', y='total', size=8, fill_color=color, line_color=color, source=source, name='total')))
        legendItems[-1][1].hover_glyph = Circle(line_width=9, line_color=color, line_alpha=0.2, fill_color=color)

        source = ColumnDataSource(data = data[airline])
        legendItems.append(([airline, "International"], 
            plot.line(x='date', y='international', line_color=color, line_width=2, line_alpha=0.6, line_dash='dotted', source=source)))
        legendItems.append(([airline, "International"], 
            plot.circle(x='date', y='international', size=5, fill_color=color, line_color=color, source=source, name='international')))
        legendItems[-1][1].hover_glyph = Circle(line_width=6, line_color=color, line_alpha=0.2, fill_color=color)

	#Create legend for airline
    legendAirlines = CategorialLegend(items=legendItems, click_policy='hide')
    plot.add_layout(legendAirlines, 'right')
    	
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

    return plot

