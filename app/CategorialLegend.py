from bokeh.core.properties import (Instance, List, String, Tuple, Override)
from bokeh.models import (Legend, LegendItem)
from bokeh.models.annotations import Annotation
from bokeh.models.renderers import GlyphRenderer

from CategorialLegendItem import CategorialLegendItem

class CategorialLegend(Annotation):
    ''' Render legend for a plot
        But can link to more renderers than used for display classs
        '''

    __implementation__ = "CategorialLegend.ts"

    items = List(Instance(CategorialLegendItem), help="""
    A list of :class:`~bokeh.model.annotations.LegendItem` instances to be
    rendered in the legend.
    This can be specified explicitly, for instance:
    .. code-block:: python
        legend = Legend(items=[
            LegendItem(label="sin(x)"   , renderers=[r0, r1]),
            LegendItem(label="2*sin(x)" , renderers=[r2]),
            LegendItem(label="3*sin(x)" , renderers=[r3, r4])
        ])
    But as a convenience, can also be given more compactly as a list of tuples:
    .. code-block:: python
        legend = Legend(items=[
            ("sin(x)"   , [r0, r1]),
            ("2*sin(x)" , [r2]),
            ("3*sin(x)" , [r3, r4])
        ])
    where each tuple is of the form: *(label, renderers)*.
    """).accepts(List(Tuple(List(String), Instance(GlyphRenderer))), lambda items: [CategorialLegendItem(labels=item[0], render=item[1]) for item in items])

    ''' Render informational legends for a plot.
    '''

    location = Either(Enum(LegendLocation), Tuple(Float, Float), default="top_right", help="""
    The location where the legend should draw itself. It's either one of
    ``bokeh.core.enums.LegendLocation``'s enumerated values, or a ``(x, y)``
    tuple indicating an absolute location absolute location in screen
    coordinates (pixels from the bottom-left corner).
    """)

    orientation = Enum(Orientation, default="vertical", help="""
    Whether the legend entries should be placed vertically or horizontally
    when they are drawn.
    """)

    border_props = Include(LineProps, help="""
    The %s for the legend border outline.
    """)

    border_line_color = Override(default="#e5e5e5")

    border_line_alpha = Override(default=0.5)

    background_props = Include(FillProps, help="""
    The %s for the legend background style.
    """)

    inactive_props = Include(FillProps, help="""
    The %s for the legend item style when inactive. These control an overlay
    on the item that can be used to obscure it when the corresponding glyph
    is inactive (e.g. by making it semi-transparent).
    """)

    click_policy = Enum(LegendClickPolicy, default="none", help="""
    Defines what happens when a lengend's item is clicked.
    """)

    background_fill_color = Override(default="#ffffff")

    background_fill_alpha = Override(default=0.95)

    inactive_fill_color = Override(default="white")

    inactive_fill_alpha = Override(default=0.7)

    label_props = Include(TextProps, help="""
    The %s for the legend labels.
    """)

    label_text_baseline = Override(default='middle')

    label_text_font_size = Override(default={'value': '10pt'})

    label_standoff = Int(5, help="""
    The distance (in pixels) to separate the label from its associated glyph.
    """)

    label_height = Int(20, help="""
    The minimum height (in pixels) of the area that legend labels should occupy.
    """)

    label_width = Int(20, help="""
    The minimum width (in pixels) of the area that legend labels should occupy.
    """)

    glyph_height = Int(20, help="""
    The height (in pixels) that the rendered legend glyph should occupy.
    """)

    glyph_width = Int(20, help="""
    The width (in pixels) that the rendered legend glyph should occupy.
    """)

    margin = Int(10, help="""
    Amount of margin around the legend.
    """)

    padding = Int(10, help="""
    Amount of padding around the contents of the legend. Only applicable when
    when border is visible, otherwise collapses to 0.
    """)

    spacing = Int(3, help="""
    Amount of spacing (in pixels) between legend entries.
    """)