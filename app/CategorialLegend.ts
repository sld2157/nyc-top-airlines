import * as p from "core/properties"
import {BBox} from "core/util/bbox"
import {LegendItem} from "./legend_item"
import {LegendView, Legend} from "models/annotations/legend";
import {Context2d} from "core/util/canvas";

type CategorialLegendItem = {item: LegendItem, active:bool}

export class CategorialLegendView extends LegendView 
{
	//A bool flag of if the legend item should be muted (ie inactive)
	protected categorialItems: CategorialLegendItem[]

	initialize(options){
		super.initialize(options)

		this.categorialItems = [];
		for (const i of this.model.items)
		{
			this.categorialItems.push({item: i, active: true});
		}
		this.render()
	}

	on_hit(sx: number, sy: number): boolean {
	    let yoffset
	    const { glyph_width } = this.model
	    const { legend_padding } = this
	    const legend_spacing = this.model.spacing
	    const { label_standoff } = this.model

	    let xoffset = (yoffset = legend_padding)

	    const legend_bbox = this.compute_legend_bbox()
	    const vertical = this.model.orientation == "vertical"

	    for (const categorialItem of this.categorialItems) {
		    const labels = categorialItem.item.get_labels_list_from_label_prop()

		    for (const label of labels) {
		        const x1 = legend_bbox.x + xoffset
		        const y1 = legend_bbox.y + yoffset

		        let w: number, h: number
		        if (vertical)
		          	[w, h] = [legend_bbox.width - 2*legend_padding, this.max_label_height]
		        else
		          	[w, h] = [this.text_widths[label] + glyph_width + label_standoff, this.max_label_height]

		        const bbox = new BBox({x: x1, y: y1, width: w, height: h})

		        if (bbox.contains(sx, sy)) {
		          	switch (this.model.click_policy) {
		            	case "hide": {
		            		categorialItem.active = !categorialItem.active;
			              	for (const r of categorialItem.item.renderers)
			                	r.visible = categorialItem.active
			              	break
		            	}
			            case "mute": {
			            	categorialItem.active = !categorialItem.active;
				            for (const r of categorialItem.item.renderers)
				                r.muted = categorialItem.active
				            break
			            }
		          	}
		          	return true
		        }

		        if (vertical)
		          	yoffset += this.max_label_height + legend_spacing
		        else
		          	xoffset += this.text_widths[label] + glyph_width + label_standoff + legend_spacing
		    }
	    }

	    return false
    }

	protected _draw_legend_items(ctx: Context2d, bbox: LegendBBox): void {
	    const {glyph_width, glyph_height} = this.model
	    const {legend_padding} = this
	    const legend_spacing = this.model.spacing
	    const {label_standoff} = this.model
	    let xoffset = legend_padding
	    let yoffset = legend_padding
	    const vertical = this.model.orientation == "vertical"

	    for (const categorialItem of this.categorialItems) {
		    const labels = categorialItem.item.get_labels_list_from_label_prop()
		    const field = categorialItem.item.get_field_from_label_prop()

		    if (labels.length == 0)
		    	continue

		    for (const label of labels) {
		        const x1 = bbox.x + xoffset
		        const y1 = bbox.y + yoffset
		        const x2 = x1 + glyph_width
		        const y2 = y1 + glyph_height

		    	if (vertical)
		        	yoffset += this.max_label_height + legend_spacing
		        else
		          	xoffset += this.text_widths[label] + glyph_width + label_standoff + legend_spacing

		        this.visuals.label_text.set_value(ctx)
		        ctx.fillText(label, x2 + label_standoff, y1 + this.max_label_height/2.0)
		        for (const r of categorialItem.item.renderers) {
			        const view = this.plot_view.renderer_views[r.id] as GlyphRendererView
			        view.draw_legend(ctx, x1, x2, y1, y2, field, label, categorialItem.item.index)
		        }

		        if (!categorialItem.active) {
		          	let w: number, h: number
		          	if (vertical)
		            	[w, h] = [bbox.width - 2*legend_padding, this.max_label_height]
		          	else
		            	[w, h] = [this.text_widths[label] + glyph_width + label_standoff, this.max_label_height]

		          	ctx.beginPath()
		          	ctx.rect(x1, y1, w, h)
		          	this.visuals.inactive_fill.set_value(ctx)
		          	ctx.fill()
		        }
		    }
	    }
  	}
}

export class CategorialLegend extends Legend
{
	type='CategorialLegend';

	default_view = CategorialLegendView;
}

