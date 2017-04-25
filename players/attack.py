""" group of four ants haunt randomly chosen foes """
from queue import Queue
from src.player_instance import PlayerInstance
from src.box_container import BoxContainer
import random

class Attack(PlayerInstance):
    def start(self):
        self.me=self._pc.get_player()
        self.groups=[[]]
        self.p_groups=[]
        self.targets=[]
        self.w,self.h=self._pc.get_width(),self._pc.get_height()
        self.block=BoxContainer(self.w, self.h)

        it=0
        for x,y,v in self._pc.get_ants():
            if v!=self.me:
                self.targets.append((x,y))
                continue

            self.groups[-1].append((x,y))
            if it==3:
                it=-1
                self.groups.append([])

            it+=1

        self.targets=self.targets[:len(self.groups)]

        for x,y in self.targets:
            self.p_groups.append(self.compute_path(x,y))

        self.dir=((-1,0), (1,0), (0,1), (0,-1))
        self.neig=((-1,0), (1,0), (0,1), (0,-1))

    def run(self, kill):
        self.block.clear()
        pass
        for i,group in enumerate(self.groups):
            for j,(x,y) in enumerate(group):
                move=self._pc.last_moves().get(x,y)
                if move!=None:
                    self.groups[i][j]=move[:2]

            if self._pc.last_kills().get(*self.targets[i])!=None:
                for x,y,v in self._pc.get_ants():
                    if v!=self.me and not (x,y) in self.targets:
                        self.targets[i]=x,y

        # update shortest paths if needed
        for i,(x,y) in enumerate(self.targets):
            new=self._pc.last_moves().get(x,y)
            if new!=None:
                self.targets[i]=new[:2]
                self.p_groups[i]=self.compute_path(new[0], new[1])


        for i,group in enumerate(self.groups):
            nx,ny=self.targets[i]

            for a,d in zip(group, self.dir):
                targetx,targety=nx+d[0],ny+d[1]
                x,y=a

                # it's on the position
                if x==targetx and y==targety:
                    continue

                # it's in the range
                if x>=nx-1 and x<=nx+1 and y>=ny-1 and y<=ny+1:
                    if x==targetx:
                        fx,fy=x,int(y+abs(targety-y)/(targety-y))
                    else:
                        fx,fy=int(x+abs(targetx-x)/(targetx-x)),y

                    if fx>=0 and fx<self.w and fy>=0 and fy<self.h \
                        and self.block.get(fx,fy)==None:
                        self._pc.move(x,y,fx,fy)
                        self.block.insert(fx,fy,True)
                else:
                    for neighbour in self.neig:
                        tmpx,tmpy=a[0]+neighbour[0],a[1]+neighbour[1]
                        if tmpx>=0 and tmpx<self.w and tmpy>=0 and tmpy<self.h and \
                            self.p_groups[i][tmpx][tmpy]!=-1 and \
                            self.p_groups[i][x][y]>self.p_groups[i][tmpx][tmpy]:
                            x,y=a[0]+neighbour[0],a[1]+neighbour[1]

                    if self.block.get(x,y)==None:
                        self._pc.move(a[0],a[1],x,y)
                        self.block.insert(x,y,True)

                        

    def compute_path(self, x, y):
        p=[ [-1 for y in range(self._pc.get_height())] for x in range(self._pc.get_width())]
        p[x][y]=0
        bfs=Queue()
        bfs.put((x,y))

        while not bfs.empty():
            curx,cury=bfs.get()
            for i,j in ((-1,0),(1,0),(0,1),(0,-1)):
                tx=curx+i
                ty=cury+j
                if tx<0 or tx>=self._pc.get_width() or \
                    ty<0 or ty>=self._pc.get_height() or \
                    self._pc.get_square(tx,ty)==-1:
                    continue

                if p[tx][ty]==-1:
                    p[tx][ty]=p[curx][cury]+1
                    bfs.put((tx,ty))

        return p
