# coding: utf-8

import json

def coloringNode(node):
	if(node["label"] != "The Drums"):
		if node["size"]<65:
			return '#70C2E8'
		elif node["size"]<75:
			return '#3B70A2'
		else:
			return '#151C48'
	return '#DC006A'
	

arquivo_json = open("dados-originais.json", 'r')
the_drums_json = json.load(arquivo_json)
nodes = the_drums_json["nodes"]
edges = the_drums_json["edges"]

nos_maiores = []
ligacoes_maiores = []

for node in nodes:
	if node["size"]>60:
		node["color"] = coloringNode(node)
		nos_maiores.append(node)
		
for edge in edges:
	for node0 in nos_maiores:
		if (edge["source"] == node0["id"]):
			for node1 in nos_maiores:
				if (edge["target"] == node1["id"]):
					ligacoes_maiores.append(edge)

dict_salvar = {"nodes": nos_maiores, "edges": ligacoes_maiores}
dict_salvar = json.dumps(dict_salvar, indent=7,sort_keys=False)

arquivo_json = open("dados-pos-script.json", "w")
arquivo_json.write(dict_salvar)
arquivo_json.close()
