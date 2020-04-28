import bpy
dir = r"C:\Users\Ahzam Ahmad\Documents\year4\cmput414\code"
f = open(dir+ "\extractions.txt", "r")
arr = {}
num=0
lines = f.readlines()
for line in lines:
    #frame number before a, coorindates after a
    a=line.find("(")
    temp = line[a:].replace(")(", ").(")
    temp = temp.split(".")
    for i in range(len(temp)):
        temp[i] = eval(temp[i])
    arr[num] = temp
    num+=1
    
first= arr[0]
for pos in first:
    bpy.ops.mesh.primitive_ico_sphere_add(location=pos, radius=3)

for collection in bpy.data.collections:
    for j in range(len(arr)-1):
        bpy.context.scene.frame_set(j)
        for i in range(len(collection.all_objects)):
            ob = collection.all_objects[i]
            ob.location = arr[j][i]
            ob.keyframe_insert(data_path="location", index=-1)
            
            