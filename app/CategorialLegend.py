from bokeh.models import (Legend, LegendItem)
from bokeh.models.renderers import GlyphRenderer

class CategorialLegend(Legend):
    ''' Render legend for a plot
        But can link to more renderers than used for display classs
        '''

    __implementation__ = "CategorialLegend.ts"