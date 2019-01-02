from bokeh.core.properties import (Instance, Int, List, String)
from bokeh.models import Model
from bokeh.models.renderers import GlyphRenderer

class CategorialLegendItem(Model):
    '''
    '''
    def __init__(self, *args, **kwargs):
        super(CategorialLegendItem, self).__init__(*args, **kwargs)

    __implementation__ = "CategorialLegendItem.ts"

    labels = List(String, help="""

        """)

    render = Instance(GlyphRenderer, help="""
    
    """)

    index = Int(default=None, help="""
    The column data index to use for drawing the representative items.
    If None (the default), then Bokeh will automatically choose an index to
    use. If the label does not refer to a data column name, this is typically
    the first data point in the data source. Otherwise, if the label does
    refer to a column name, the legend will have "groupby" behavior, and will
    choose and display representative points from every "group" in the column.
    If set to a number, Bokeh will use that number as the index in all cases.
    """)
