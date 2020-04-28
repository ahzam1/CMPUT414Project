import operator
#module needed for adding tuples

#open our file that contains landmarks and their positions
f = open("extractions.txt", "r")
lines = f.readlines()
f.close()

numLines = len(lines)
lineNum=0
missed=[]
for line in lines:
	if "(" not in line:
		#missed detection, need to interpolate.
		missed.append(False)
	else:
		missed.append(True)
	lineNum+=1

# for loop to change the strings into readable and usable tuples
for i in range(len(lines)):
	line = lines[i]
	if "(" not in line:
		continue
	temp = line.replace(")(", ").(")
	temp = temp.split(".")
	for j in range(len(temp)):
		temp[j] = eval(temp[j])
	lines[i] = temp

#start iterating through our missed detections
n=0
while n<len(missed):
    if(not missed[n]):
		#missed detection
		#look for previous and next detection for interpolation
        c=n
        prev=n
        while c!=0:
            if(missed[c]):
                prev=c
                break
            c-=1
        c=n
        future =n
        while c != numLines:
            if(missed[c]):
                future=c
                break
            c+=1


        if(future==prev and future==n):
            #no face detected before and after, do nothing and exit.
            exit()
        if(prev==n and future !=n):
            #no prior face detected, but future was so we can make all prior frames equivalent to future
            while prev> -1:
                lines[prev] = lines[future]
                missed[prev]=True
                prev-=1
            n+=1
            continue
        if(future ==n):
            #prior found, future not, so just keep face at its last known position.
            while future< numLines:
                lines[future] = lines[prev]
                missed[future]=True
                future+=1
            n+=1
            continue

		#if made it here, future and prior found, need to interpolate between the two.
        dist = future-prev
        #no of frames to tween.

        pf = lines[prev]
        ff = lines[future]
        #have both frames that we need to interpolate between
        diff = []
        for i in range(len(pf)):
            #calculating the amount of movement per frame, per landmark.
            temp1= int((ff[i][0]-pf[i][0])/dist)
            temp2= int((ff[i][1]-pf[i][1])/dist)
            diff.append((temp1,temp2,0))
        for j in range(prev+1, future):
            pframe = lines[j-1]
            #getting the prior frame
            cframe=[]
            missed[j]=True
            for k in range(len(pf)):
                #adding the prior frame and movement per frame, to create current frame.
                cframe.append(tuple(map(operator.add, pframe[k], diff[k])))
            #updating the missed detection
            lines[j] = cframe
				

    n+=1
f = open("extractions.txt", "w")
print(lines[0])
for line in lines:
    print(line)
    for e in line:
        f.write(str(e))
    f.write("\n")
f.close()