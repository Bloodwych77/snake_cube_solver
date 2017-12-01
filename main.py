class segment:
	def __init__(self,num,xyz,len,dir,chr):
		self.num = num #Starts at 1 (0 reserved for empty space)
		self.xyz = xyz
		self.len = len
		self.dir = dir #[xdir,ydir,zdir] where xdir,ydir,or zdir = +1,-1,or False (False means impossible direction) 
		self.chr = chr #A character selected from the puzzleseq string
	def __repr__(self):
		return self.chr*self.len

puzzleseq = (3,1,2,1,1,3,1,2,1,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,2,3,1,1,1,3,1,2,1,1,1,1,1,1,1,1,1,3,1)
	#Puzzle sequence to be solved
	
mychr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	#Reference for segment identification (A = first, B = second,...)

axisstr = 'XYZ'		#Labels for 3-axiis
	
space = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],	#[x]  [y]  [z]
		 [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],	#[row][col][hgt]
         [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
         [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]

def print444(matrix1):	#Print a 4x4x4 matrix in perspective format
	line = ""
	for y in list(range(4)):
		for z in list(range(4)):
			for x in list(range(4)):
				if matrix1[x][y][z] == 0:
					char = ' '
				else:
					char = matrix1[x][y][z]
				if y == 0:
					if x < 3:
						line = line + "| "*z + char + "--"*(4-z)
					elif x == 3:
						line = line + "| "*z + char
				elif y == 3:
					if x == 0:
						line = line + "  "*z + char + "--"*(4-z)
					elif x == 1 or x == 2:
						line = line + "--"*z + char + "--"*(4-z)
					elif x == 3:
						line = line + "--"*z + char + " |"*(3-z)
				else:
					if x < 3:
						line = line + "| "*z + char + "--"*(4-z)
					elif x == 3:
						line = line + "| "*z + char + " |"*(3-z)
			print(line)
			line = ""
		if y < 3:
			print("| | | |  "*4)
	
def printlin(array1):
	colloc = 0
	str = ""
	for n in list(range(len(array1))):
		if array1[n].num % 2 == 1:	#Odd segment prints down
			str = str + ("\n" + " "*(colloc-1) + array1[n].chr)*array1[n].len
		else:						#Even prints right
			str = str + array1[n].chr*array1[n].len
			colloc = colloc + array1[n].len
	print(str)		 

def zeromat(matrix1):	#Set all values of a 4x4x4 matrix to 0
	for x in list(range(4)):
		for y in list(range(4)):
			for z in list(range(4)):
				matrix1[x][y][z] = 0
	return matrix1
	
def copymat(matrix1):	#Create a new copy of a 4x4x4 matrix, not a pointer
	matrix2=matrix1[:]
	for x in list(range(4)):
		matrix2[x]=matrix1[x][:]
		for y in list(range(4)):
			matrix2[x][y]=matrix1[x][y][:]
	return matrix2
	
def axisof(array1):					#Returns the index of the axis of the first 1 or -1 in array1
	if -1 in array1:				#0 = X-axis
		return array1.index(-1)		#1 = Y-axis
	elif 1 in array1:				#2 = Z-axis
		return array1.index(1)		#returns False if array1 doesn't contain any directions
	else:
		return None
		
def laydown(matrix1, array1, xyz, dir, sn):					#Returns the ending [x,y,z] after a segment is laid
	for n in list(range(array1[sn].len)):					#For each character in segment
		matrix1[xyz[0]][xyz[1]][xyz[2]] = array1[sn].chr	#Store the next identifying character in the matrix
		print('matrix1[%i][%i][%i]=%s' % (xyz[0],xyz[1],xyz[2],matrix1[xyz[0]][xyz[1]][xyz[2]]))
		if n < array1[sn].len-1:
			xyz = xyzmove(xyz,dir,1)						#Move one unit in the 'dir' direction
	return xyz
	
def pickup(matrix1, array1, xyz, dir, sn):					#Returns the ending [x,y,z] after a segment is lifted
	oppdir = dir
	oppdir[axisof(dir)] = -dir[axisof(dir)]
	for n in list(range(array1[sn].len)):					#For each character in segment
		matrix1[xyz[0]][xyz[1]][xyz[2]] = 0					#Reset identifying character in the matrix to 0
		print('matrix1[%i][%i][%i]=%s' % (xyz[0],xyz[1],xyz[2],matrix1[xyz[0]][xyz[1]][xyz[2]]))
		if n < array1[sn].len-1:
			xyz = xyzmove(xyz,oppdir,1)						#Move one unit in the opposite 'dir' direction
	return xyz

def xyzmove(xyz,dir,num):
	for n in list(range(num)):
		if xyz[axisof(dir)]+dir[axisof(dir)] in list(range(4)):
			xyz[axisof(dir)] = xyz[axisof(dir)]+dir[axisof(dir)]
		else:
			xyz[axisof(dir)] = False
	return xyz

def changedir(dir,axis):
	if dir[axis] == 1:
		input("Try the -dir...")
		dir[axis] = -1
	else:
		input("-dir failed, set axis to False...")
		dir[axis] = False
		if 0 in dir:									#Select next axis to test
			dir[dir.index(0)] = 1
	return dir
	
	
def backupsn(array1, sn):	#Back up the sn to the last possible sn or return False if none exists.
	looking = True		#Needs improvement
	while looking:
		if array1[sn].dir == [False,False,False]:
			if sn > 0:
				array1[sn] = segment(sn,[0,0,0],puzzleseq[sn],[0,0,0],mychr[sn])
				sn = sn - 1
			else:
				sn = False
				looking = False
		else:
			looking = False
	return sn

def inputxyz(x,y,z):
	try: x = int(input('Start at X='))
	except:	x = 0
	try: y = int(input('Start at Y='))
	except:	y = 0
	try: z = int(input('Start at Z='))
	except:	z = 0
	return [x,y,z]
			

s = list(range(len(puzzleseq)))		#Setup segment array 's'
for n in s:							#using puzzleseq and mychr
	s[n] = segment(n,[0,0,0],puzzleseq[n],[0,0,0],mychr[n])
	
def solve3d(array1):
	solution = copymat(space)
	sn = 0		#Segment number index (0=first segment)
	solved = False
	while not solved:
		newstart = False
		badmove = False
		chk_axis = 0
		[x,y,z] = inputxyz(0,0,0)
		while not newstart:
			chk_xyz = [x,y,z]										#Reset looking direction by setting to actual position
			if s[sn].dir == [ 0, 0, 0]:									#This is a new decision point
				if sn > 0:													#Not the first puzzle piece
					s[sn].dir[axisof(s[sn-1].dir)] = False						#Rule out the last movement axis
					s[sn].dir[(axisof((s[sn-1].dir))+1)%3] = 1					#and select the next '0' axis
					chk_xyz = xyzmove([x,y,z],s[sn].dir,1)						#Look one block in the 'dir' direction
				else:														#For the first piece
					s[sn].dir = [ 1, 0, 0]										#Check in the +X direction
			elif 1 in s[sn].dir or -1 in s[sn].dir:						#Select next looking direction
				if sn > 0:													#Not the first piece
					chk_xyz = xyzmove([x,y,z],s[sn].dir,1)						#Look one block in the 'dir' direction
			else:														#All 'dir' tested and failed
				sn = backupsn(s,sn)											#Backup to previous non-fail segment 
				if sn == False:												#If backed up to first segment
					sn = 0														#Reset segment index
					newstart = True												#Restart at a new [x,y.z]
			chk_axis = axisof(s[sn].dir)								#Set chk_axis to active axis
			occupied = False
			print('Move in the %s%s direction' % ('-' if s[sn].dir[chk_axis]<0 else '+', axisstr[chk_axis]))
			print('Final %s pos=%i' % (axisstr[chk_axis], int(chk_xyz[chk_axis])+int(s[sn].dir[chk_axis])*(s[sn].len-1)))
			input("Enter...")
			if (chk_xyz[chk_axis]+(s[sn].dir[chk_axis]*(s[sn].len-1))) in list(range(4)):
																		#Check if OOB
				chk_xyz_tmp = chk_xyz[:]
				for n in list(range(s[sn].len)):							#Check overlap in seg dir for len of seg
					if solution[chk_xyz_tmp[0]][chk_xyz_tmp[1]][chk_xyz_tmp[2]] != 0:		#Overlap check
						occupied = True
					chk_xyz_tmp = xyzmove(chk_xyz_tmp,s[sn].dir,1)
				if occupied == True:										#Try opposite dir or back out of move
					input("Occupied space...")
					s[sn].dir = changedir(s[sn].dir,chk_axis)
				else:
					print('[chk_x,chk_y,chk_z]=%s' % [chk_xyz[0],chk_xyz[1],chk_xyz[2]])
					input ("Enter...")
					s[sn].xyz = [x,y,z]
					[x,y,z] = laydown(solution,s,[chk_xyz[0],chk_xyz[1],chk_xyz[2]],s[sn].dir,sn)
					print('[x,y,z]=%s' % [x,y,z])
					input ("Enter...")
			else:
				badmove = True											#OOB
				s[sn].dir = changedir(s[sn].dir,chk_axis)
			if not badmove:
				if sn < len(puzzleseq):									#Increment decision point if we aren't at the last piece
					sn = sn + 1
			else:
				badmove = False
				sn_bad = sn
				sn = backupsn(s,sn)
				for n in list(range(sn_bad,sn,-1)):
					[x,y,z] = pickup(solution,s,[x,y,z],s[n].dir,n)
				if sn == False:
					sn = 0
					newstart = True
			print('\nCurrent segment:',)
			print(s[sn])
			print('Remaining puzzle:',)
			printlin(s[(sn+1):])
			print444(solution)
			input('Enter to continue...')
	return solution
	
print("With this flat layout:")
printlin(s)
finalsol = solve3d(s)
print("We get this solution:")	
print444(finalsol)
junk = input("Press enter to exit...")
