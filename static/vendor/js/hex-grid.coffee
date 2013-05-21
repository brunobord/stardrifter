window.HexGrid =
  class HexGrid
    degreesToRadians: (degrees) -> degrees * Math.PI / 180

    constructor: (@cols, @rows, @size, @padding)->
      @r = @size * Math.cos(this.degreesToRadians(30))
      @h = @size * Math.sin(this.degreesToRadians(30))
      @d = @padding / 2 / Math.tan(this.degreesToRadians(30))

      this.renderHexTile()

    renderHexTile: ->
      tileWidth  = (4 * @r) + (2 * @padding)
      tileHeight = (2 * @h) + (2 * @size) + (2 * @d)

      vertices = this.calculateHexTile()

      d3
        .select("#hex-tile")
        .attr("width",  tileWidth)
        .attr("height", tileHeight)

      polygon = d3.select("#hex-tile").selectAll("polygon").data(vertices)
      polygon.enter().append("svg:polygon")
      polygon.attr("points", (d, i) -> d.join(" "))

      d3
        .select("#hex-grid")
        .attr("width",  tileWidth  * @cols)
        .attr("height", tileHeight * @rows)

    calculateHexTile: ->
      originX = -@r - (@padding / 2)
      originY = -@h - (@size / 2)

      vertices = []

      for row in [0...3]
        for col in [0...3]
          [x, y] = this.calculateXY(originX, originY, col, row)
          vertices.push(this.calculateHexVertices(x, y))

      vertices

    calculateXY: (x, y, col, row) ->
      width  = (2 * @r) + @padding
      height = @size + @h + @d

      [
        x + (col * width) + ((row % 2) * (width / 2))
        y + (row * height)
      ]

    calculateHexVertices: (x, y) ->
      [
        [x,      y                  ]
        [x + @r, y + @h             ]
        [x + @r, y + @size + @h     ]
        [x,      y + @size + @h + @h]
        [x - @r, y + @size + @h     ]
        [x - @r, y + @h             ]
      ]
