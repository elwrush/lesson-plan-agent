#import "/lib/typst/lib.typ": *

// Custom header for summer courses
#let summer_header() = {
  v(0.2cm)
  align(center)[
    #set block(stroke: none)
    #set image(width: 100%)
    // Make sure paths to images resolve from the project root correctly
    #image("/SUMMER-CONVERSION/images/worksheet_header.png")
  ]
  v(0.2cm)
}
