
recursion_depth = 0
def virus_duple(num_virus):
	global recursion_depth
	if num_virus >= 1000000000:
		return
	num_virus = num_virus * 2
	recursion_depth += 1
	virus_duple(num_virus)

virus_duple(2)

print(recursion_depth)
#print(f"it will take{recursion_depth} to reach {num_virus}")

# recursion_depth2 = 0
# vr = 1
# while vr<1000000000:
# 	vr = vr * 2
# 	recursion_depth2 +=1
# 	if vr >1000000000:
# 		print(vr)

# print(recursion_depth2)
