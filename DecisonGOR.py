import time
import datetime

class TreeNode:
	def __init__(self, id, N, M):
		self.id = id   # 编号
		self.name = -1  # 对应元件编号
		self.v = [0] * (M + 1)  # v/w为标签，初始化长度为 M+1 的数组
		self.w = [0] * (M + 1)
		self.edge = [None] * (M + 1)  # 边所连接的子节点
		self.pListNode = []  # 存放父节点
		self.pListWay = []  # 存放与父节点对应相连的边


Ordered = [11, 23, 28, 4, 12, 18, 2, 21, 22, 27, 13, 5, 15, 26, 7, 14, 17, 6, 9, 10, 29, 19, 8, 20, 3, 1, 24, 16, 25]
N = 29
M = 7
ZERO = TreeNode(0, N, M)
ZERO.name = 0

ONE = TreeNode(-1, N, M)
ONE.name = -1

cSet = [[1,2,3,4,5], [1,6,7,8,9], [1,10,11,12,13], [1,14,15,16,17], [1,18,19,20,21], [1,22,23,24,25], [1,26,27,28,29]]
kSet = [4,4,4,4,4,4,4]
nSet = [5,5,5,5,5,5,5]

t1 = time.time()
# t1 = datetime.datetime.now()
currNodeName = Ordered[0]
MDDL = [[] for _ in range(N+2)]
cntId = 1


def addLabel(x, y, j):  # 根据父节点与所连的边给子节点添加标签
	i = 1
	while i <= M:
		if x.name not in cSet[i-1]:
			y.v[i], y.w[i] = x.v[i], x.w[i]
		elif (x.name in cSet[i-1] and x.v[i] == 0):
			y.v[i], y.w[i] = x.v[i], x.w[i]
		else:
			if j == 0 or i < j:
				y.v[i], y.w[i] = x.v[i] - 1, x.w[i] - 1
				if y.v[i] == 0:
					y.w[i] = 0
			else:
				y.v[i], y.w[i] = x.v[i], x.w[i] - 1
		i += 1

def addSubNode(y, z): #根据相关关系给父节点添加子节点
	global cntId
	#edge-0
	flag = True
	for i in range(1, M + 1):
		if y.v[i] != 0 and y.v[i] != 1:
			flag = False
			break
		if y.v[i] == 1 and y.name not in cSet[i-1]:
			flag = False
			break
	if flag:
		#连接到汇聚节点'0'
		y.edge[0] = ZERO
		z.append(ZERO)
	else:
		z1 = TreeNode(cntId, N, M)
		cntId += 1
		z1.name = Ordered[Ordered.index(y.name)+1]
		z1.pListWay.append(0)
		z1.pListNode.append(y)
		z.append(z1)
		y.edge[0] = z1

	#edge-M
	if y.v[M] == y.w[M] and y.w[M] != 0 and y.name in cSet[M-1]:
		#连接到汇聚节点'1'
		for i in range(1, M + 1):
			y.edge[i] = ONE
		return
	elif y.name not in cSet[M-1] or y.v[M] == 0:
		if y.edge[0] == ZERO:
			y.edge[M] = ZERO
		else:
			for i in range(len(z)):
				if z[i].id == y.edge[0].id:
					z[i].pListNode.append(y)
					z[i].pListWay.append(M)
					y.edge[M] = z[i]
					break
	else:
		z1 = TreeNode(cntId, N, M)
		cntId += 1
		z1.name = Ordered[Ordered.index(y.name)+1]
		z1.pListWay.append(M)
		z1.pListNode.append(y)
		z.append(z1)
		y.edge[M] = z1

	#other edge
	if M == 1:
		return
	j = M - 1 #从后往前
	while j > 0:
		if y.v[j] == y.w[j] and y.w[j] != 0 and y.name in cSet[j-1]:
			for i in range(1, j + 1):
				y.edge[i] = ONE; #print(y.name in cSet[j-1])
			return
		elif y.name not in cSet[j-1] or y.v[j] == 0:
			if y.edge[j+1] == ZERO:
				y.edge[j] = ZERO
			else:
				for i in range(len(z)):
					if z[i].id == y.edge[j+1].id:
						z[i].pListNode.append(y)
						z[i].pListWay.append(j)
						y.edge[j] = z[i]
						break
		else:
			z1 = TreeNode(cntId, N, M)
			cntId += 1
			z1.name = Ordered[Ordered.index(y.name)+1]
			z1.pListWay.append(j)
			z1.pListNode.append(y)
			z.append(z1)
			y.edge[j] = z1
		j -= 1	

n = 1
while n <= N:
	print('n=:', n)
	if n == 1:
		idN = 1
		newNode = TreeNode(idN, N, M)
		newNode.name = currNodeName
		for i in range(1, M + 1):
			newNode.v[i] = kSet[i-1]
			newNode.w[i] = nSet[i-1]	
		MDDL[n].append(newNode)
		#print(MDDL[n][0].name, MDDL[n][0].id)
	else:
		x = 0
		while x < len(MDDL[n]):
			if MDDL[n][x].id == 0 or MDDL[n][x].id == -1 or MDDL[n][x].id == -2:
				x += 1
				continue
			j = 0
			while j < len(MDDL[n][x].pListNode):
				p = MDDL[n][x].pListNode[j]
				c = MDDL[n][x]
				e = MDDL[n][x].pListWay[j]
				addLabel(p, c, e)
				j += 1
			x += 1
	#if n == 3:
	#	for i in range(len(MDDL[n])):
	#		print(MDDL[n][i].id, MDDL[n][i].name, MDDL[n][i].v[2], MDDL[n][i].w[2])
	#		for j in range(len(MDDL[n][i].pListNode)):
	#			print(MDDL[n][i].pListNode[j].name, MDDL[n][i].pListNode[j].id, MDDL[n][i].pListWay[j])
	if n > 1:
		i1 = 0
		lenM = len(MDDL[n]);
		while i1 < lenM:
			if MDDL[n][i1].id == 0 or MDDL[n][i1].id == -1 or MDDL[n][i1].id == -2: #汇聚节点或者已经被确认是相同标签节点
				i1 += 1
				continue
			j1 = i1 + 1;
			while j1 < lenM:
				if MDDL[n][i1].id == 0 or MDDL[n][i1].id == -1 or MDDL[n][i1].id == -2: #汇聚节点或者已经被确认是相同标签节点
					j1 += 1
					continue
				flag = True
				for i in range(1, M + 1):
					if not (MDDL[n][i1].v[i] == MDDL[n][j1].v[i] and MDDL[n][i1].w[i] == MDDL[n][j1].w[i]):
						flag = False
						break
                                #print(flag)
				if flag: #编号和标签都相同的节点
					for i in range(len(MDDL[n][j1].pListNode)):
						pNode = MDDL[n][j1].pListNode[i]
						pWay = MDDL[n][j1].pListWay[i]
						faNode = None
						for k1 in range(len(MDDL[n-1])):
							if MDDL[n-1][k1].id != 0 and MDDL[n-1][k1].id != -1 and MDDL[n-1][k1].id != -2 and pNode.id == MDDL[n-1][k1].id:
								faNode = MDDL[n-1][k1]
								break
						MDDL[n][i1].pListNode.append(pNode)
						MDDL[n][i1].pListWay.append(pWay)
						faNode.edge[pWay] = MDDL[n][i1]
					MDDL[n][j1].id = -2
					#print('j1 =', j1)
				j1 += 1
			i1 += 1;

	#生成子节点
	ai1 = 0
	cntId = 1
	#print(ai1, len(MDDL[n]))
	while ai1 < len(MDDL[n]):
		#print('hahaha')
		if MDDL[n][ai1].id == 0 or MDDL[n][ai1].id == -1 or MDDL[n][ai1].id == -2:
			ai1 += 1
			continue
		#print('n+1:', (n + 1))
		addSubNode(MDDL[n][ai1], MDDL[n+1])
		#print('cntId:', cntId)
		ai1 += 1
	n += 1

#合并同构节点
n = N
while n > 1:
	lenM = len(MDDL[n])
	i1 = 0
	while i1 < lenM:
		if MDDL[n][i1].id == 0 or MDDL[n][i1].id == -1 or MDDL[n][i1].id == -2:
			i1 += 1
			continue
		j1 = i1 + 1
		while j1 < lenM:
			if MDDL[n][j1].id == 0 or MDDL[n][j1].id == -1 or MDDL[n][j1].id == -2:
				j1 += 1
				continue

			flag = True
			for i in range(0, M + 1):
				#print('n:', n, 'i:', i)
				#print(MDDL[n][i1].id, MDDL[n][j1].id)
				#print(MDDL[n][i1].edge[i] == None)
				#print(MDDL[n][j1].edge[i] == None)
				if MDDL[n][i1].edge[i].id != MDDL[n][j1].edge[i].id:
					flag = False
					break
			if flag: #同构节点
				for i in range(len(MDDL[n][j1].pListNode)):
					pNode = MDDL[n][j1].pListNode[i]
					pWay = MDDL[n][j1].pListWay[i]
					faNode = None
					for k1 in range(len(MDDL[n-1])):
						if MDDL[n-1][k1].id != 0 and MDDL[n-1][k1].id != -1 and MDDL[n-1][k1].id != -2 and pNode.id == MDDL[n-1][k1].id:
							faNode = MDDL[n-1][k1]
							break
					MDDL[n][i1].pListNode.append(pNode)
					MDDL[n][i1].pListWay.append(pWay)
					faNode.edge[pWay] = MDDL[n][i1]
					MDDL[n][j1].id = -2
			j1 += 1
		i1 += 1
	n -= 1

#t2 = time.time()
#t2 = datetime.datetime.now()

ans = 0
otherNum = 0  #冗余节点
for n in range(1, N + 1):
	for i in range(len(MDDL[n])):
		if MDDL[n][i].id == 0 or MDDL[n][i].id == -1 or MDDL[n][i].id == -2:
			continue
		ans += 1
		flag = True
		for j in range(1, M + 1):
			if MDDL[n][i].edge[j].id != MDDL[n][i].edge[j-1].id:
				flag = False
				break
		if flag:
			otherNum += 1

t2 = time.time()
print('非汇聚节点数为:', ans - otherNum)
print('总节点数为:', ans)
print('冗余节点数为:', otherNum)
print('时间为', (datetime.datetime.fromtimestamp(t2) - datetime.datetime.fromtimestamp(t1)).microseconds / 1000.0, 'ms')
print(datetime.datetime.fromtimestamp(t1), datetime.datetime.fromtimestamp(t2), (datetime.datetime.fromtimestamp(t2) - datetime.datetime.fromtimestamp(t1)))
#print('时间为', (t2 - t1).seconds * 1000, 'ms')
#for n in range(1, N + 1):
#	for i in range(len(MDDL[n])):
#		if MDDL[n][i].id == 0 or MDDL[n][i].id == -1 or MDDL[n][i].id == -2:
#			continue
		
		#for j in range(0, M + 1):
		#	print(MDDL[n][i].name, '(', MDDL[n][i].id, ')-', j, '-', MDDL[n][i].edge[j].name, '(', MDDL[n][i].edge[j].id, ')')

