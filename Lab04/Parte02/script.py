import os, json

############# Mapping every artist/group to a genre list
data = json.load(open("mytop50.json", 'r'))

genreMap = {}

for artist in data["items"]:
	for gen in artist["genres"]:
		if not gen in genreMap.keys():
			genreMap[gen] = []
		genreMap[gen].append(artist)

###### FILTERING GENRES WITH LESS THAN 5 MEMBERS OR MORE THAN 10

for k in genreMap.keys():
	if len(genreMap[k]) < 4 or len(genreMap[k]) > 10:
		genreMap.pop(k)

genreMap.pop("rap metal")
genreMap.pop("indie pop")
genreMap.pop("post-grunge")
genreMap.pop("alternative dance")
genreMap.pop("alternative metal")

for k in genreMap.keys():
	for a in genreMap[k]:
		keys = a.keys()
		if ("href" in keys):
			a.pop("href")
		if ("type" in keys):
			a.pop("type")
		if ("uri" in keys):
			a.pop("uri")
		if ("external_urls" in keys):
			a["url"] = a["external_urls"]["spotify"]
			a.pop("external_urls")
		if ("images" in keys):
			a["img"] = a["images"][-1]["url"]
			a.pop("images")
		if ("followers" in keys):
			if (type(a["followers"]) != int):
				number = a["followers"]["total"]
				a.pop("followers")
				a["followers"] = number


###### SETTING THE FINAL JSON

nodelink = {}
nodelink["nodes"] = []
nodelink["edges"] = []

###### CREATING NODES

added = []

for k in genreMap.keys():
	bool = False
	for node in genreMap[k]:
		if (not node["id"] in added):
			nodelink["nodes"].append(node)
			added.append(node["id"])

###### CREATING LINKS
# EVERY OBJECT IN A GENRE IS LINKED TO ALL OTHER OBJECTS IN THE SAME CATEGORY

for i in range(len(nodelink["nodes"])):
	node = nodelink["nodes"][i]
	for genre in genreMap.keys():
		for j in range(i+1, len(nodelink["nodes"])):
			node2 = nodelink["nodes"][j]
			if genre in node2["genres"] and genre in node["genres"]:
				link = {}
				link["source"] = node["id"]
				link["target"] = node2["id"]
				link["type"] = genre
				nodelink["edges"].append(link)

with open("result.json", 'w') as outfile:
	json.dump(nodelink, outfile)
