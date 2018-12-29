from flask import Flask, render_template
from nvd3 import pieChart

app = Flask(__name__)

@app.route('/')
def index():
	type = 'pieChart'
	chart = pieChart(name=type, color_category='category20c', height=450, width=450)
	chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")

	xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
	ydata = [3, 4, 0, 1, 5, 7, 3]

	extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
	chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
	chart.buildcontainer()
	htmlchart = chart.htmlcontent
	return render_template('welcome.html', chart=htmlchart)

@app.route('/year/<int:year>')
def year(year):
	return 'This will display information for year %d' % year