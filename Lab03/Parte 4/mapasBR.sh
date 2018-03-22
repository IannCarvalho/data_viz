#!/bin/bash

# a expressão js que decide os fills baseados em uma escala
# EXP_ESCALA='z = d3.scaleSequential(d3.interpolateViridis).domain([0, 100]),
#             d.features.forEach(f => f.properties.fill = z(f.properties["Percentual Aprendizado Adequado (%)"])),
#             d'
EXP_ESCALA='z = d3.scaleThreshold().domain([43540, 72273, 127131, 241929, 882183, 499375401]).range(d3.schemePurples[5]),
            d.features.forEach(f => f.properties.fill = z(f.properties["2012"])),
            d'

ndjson-map -r d3 -r d3=d3-scale-chromatic \
  "$EXP_ESCALA" \
< geo4-br-e-ideb-simplificado.json \
| ndjson-split 'd.features' \
| geo2svg -n --stroke none -w 1000 -h 600 \
  > aprendizagem-na-pb-choropleth.svg
