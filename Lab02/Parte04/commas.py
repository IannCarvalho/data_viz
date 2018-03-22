data = open("rs.csv", 'r')
lines = data.readlines()

hora_antiga = "06"
linha_nova = ""
mulheres_ciclistas = 0
homens_ciclistas = 0
mulheres_pedestres = 0
homens_pedestres = 0
novas_linhas=[]
novas_linhas.append(lines[0])
	
for i in range(len(lines)):
	if(lines[i][0] != "h"):
		if(lines[i][0]+lines[i][1]==hora_antiga):
			array = lines[i].split(",")
			mulheres_ciclistas += int(array[1])
			homens_ciclistas += int(array[2])
			mulheres_pedestres += int(array[3])
			homens_pedestres += int(array[4])
		else:
			mulheres_ciclistas = mulheres_ciclistas/4
			homens_ciclistas = homens_ciclistas/4
			mulheres_pedestres = mulheres_pedestres/4
			homens_pedestres = homens_pedestres/4
			
			linha_nova = "%s,%d,%d,%d,%d\n" %(hora_antiga,mulheres_ciclistas,homens_ciclistas,mulheres_pedestres,homens_pedestres)
			novas_linhas.append(linha_nova)
			hora_antiga = lines[i][0]+lines[i][1]
			mulheres_ciclistas = int(array[1])
			homens_ciclistas = int(array[2])
			mulheres_pedestres = int(array[3])
			homens_pedestres = int(array[4])
			

mulheres_ciclistas = mulheres_ciclistas/4
homens_ciclistas = homens_ciclistas/4
mulheres_pedestres = mulheres_pedestres/4
homens_pedestres = homens_pedestres/4
						
linha_nova = "%s,%d,%d,%d,%d\n" %(hora_antiga,mulheres_ciclistas,homens_ciclistas,mulheres_pedestres,homens_pedestres)
novas_linhas.append(linha_nova)

to_write = "".join(novas_linhas)

with open("result.csv",'w') as result:
	result.write(to_write)

data.close()
