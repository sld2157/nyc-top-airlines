import {Model} from "model"
import {Legend} from "models/annotations/legend"
import {GlyphRenderer} from "models/renderers/glyph_renderer"
import * as p from "core/properties"

export namespace CategorialLegendItem {
  export interface Attrs extends Model.Attrs {
    labels: string[] | null
    render: GlyphRenderer
    index: number | null
  }

  export interface Props extends Model.Props {}
}

export interface CategorialLegendItem extends CategorialLegendItem.Attrs {}

export class CategorialLegendItem extends Model {

  properties: CategorialLegendItem.Props

  legend: Legend | null

  constructor(attrs?: Partial<CategorialLegendItem.Attrs>) {
    super(attrs)
  }

  static initClass(): void {
    this.prototype.type = "CategorialLegendItem"

    this.define({
      labels:     [ p.Array, [] ],
      render: [ p.Any,   null   ],
      index:     [ p.Number,     null ],
    })
  }

  initialize(): void {
    super.initialize()
    this.legend = null
    this.connect(this.change,
      () => { if (this.legend != null) this.legend.item_change.emit() })
  }
}
CategorialLegendItem.initClass()