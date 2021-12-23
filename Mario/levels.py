from os import walk

pos_list = [(110,400),(300,220),(480,610),(610,350),(880,210),(1050,400)]
def level_data():
	final_dic = {}
	for (dirpaths, dirnamess, filenamess) in walk("Levels/"):
		
		
		for level in dirnamess[:-2]:
			#print(level)
			dics = {}
			for (a, b, c) in walk(f"Levels/{level}"):
				 new_list = [f"Levels/{level}/{i}" for i in c]
				 #dics[int(level)] = new_list
			
			for item in new_list:
				dics[item.split("_",2)[2][:-4]] = item
			
			dics["node_pos"] = pos_list[int(level)]
			dics["node_graphics"] = f"graphics/overworld/{level}"
			if int(level) < len(dirnamess[:-2])-1:
				dics["unclock"] = int(level) + 1
			else:
				dics["unclock"] = int(level)
			final_dic[int(level)] = dics
			
	return final_dic
levels = level_data()
# def import_file(path):
# 	level_0 = {}
# 	for (dirpath, dirnames, filenames) in walk(path):
# 	    for filename in filenames:
# 	    	level_0[filename[9:-4]] = f"{dirpath}{filename}"
# 	return level_0
# level_0 = import_file("Levels/2/")
# #print(level_0)
# level_0["node_pos"] = (110,400)
# level_0["unclock"] = 1
# level_0["node_graphics"] = "graphics/overworld/0"
# level_1 = import_file("Levels/1/")
# level_1["node_pos"] = (300,220)
# level_1["unclock"] = 2
# level_1["node_graphics"] = "graphics/overworld/1"
# level_2 = import_file("Levels/0/")
# level_2["node_pos"] = (480,610)
# level_2["unclock"] = 3
# level_2["node_graphics"] = "graphics/overworld/2"
# level_3 = import_file("Levels/2/")
# level_3["node_pos"] = (610,350)
# level_3["unclock"] = 4
# level_3["node_graphics"] = "graphics/overworld/3"
# level_4 = import_file("Levels/1/")
# level_4["node_pos"] = (880,210)
# level_4["unclock"] = 5
# level_4["node_graphics"] = "graphics/overworld/4"
# level_5 = import_file("Levels/0/")
# level_5["node_pos"] = (1050,400)
# level_5["unclock"] = 5
# level_5["node_graphics"] = "graphics/overworld/5"
