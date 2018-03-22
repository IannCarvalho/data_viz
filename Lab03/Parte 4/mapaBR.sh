#!/bin/bash

# Cria um geojson simplificado e quantizado dos municípios da PB + dados do QEDU

# OBTER E TRANSFORMAR OS DADOS ======================
# Baixa e descompacta
# curl 'ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2016/UFs/PB/pb_municipios.zip' -o pb_municipios.zip
# unzip br_municipios.zip

# # Cria geometria projetada
# shp2json BRMUE250GC_SIR.shp --encoding 'utf8' \
#   | geoproject \
#     'd3.geoOrthographic().rotate([54, 14, -2]).fitSize([1000, 600], d)' \
#     > geo1-br_municipios_projetado.json

# Dados de aprendizagem do QEDU
dsv2json \
  -r ',' \
  -n \
  < result.csv \
  > dado1-ideb-br.ndjson

# JOIN Geometria, Dado ======================
# organiza geometria
ndjson-split 'd.features' \
  < geo1-br_municipios_projetado.json \
  | ndjson-map 'd.cidade = +d.properties.GEOCODIGO, d' \
  > geo2-br_municipios.ndjson

# organiza variável
ndjson-map 'd.cidade = +d.IBGE, d' \
  < dado1-ideb-br.ndjson \
  > dado2-ideb-br-comchave.ndjson

# o join
# 1. left join (como em SQL)
# 2. o resultado do join é um array com 2 objetos por linha
# 3. o ndjson-map volta a um objeto por linha
EXP_PROPRIEDADE='d[0].properties = Object.assign({}, d[0].properties, d[1]), d[0]'
ndjson-join --left 'd.cidade' \
  geo2-br_municipios.ndjson \
  dado2-ideb-br-comchave.ndjson \
  | ndjson-map \
    "$EXP_PROPRIEDADE" \
  > geo3-municipios-e-ideb.ndjson

# SIMPLIFICA E QUANTIZA ======================
geo2topo -n \
  tracts=- \
< geo3-municipios-e-ideb.ndjson \
| toposimplify -p 1 -f \
| topoquantize 1e5 \
| topo2geo tracts=- \
> geo4-br-e-ideb-simplificado.json
