""" five ants go the shorthest path to the nest, rest is random"""
from queue import Queue
from src.player_instance import PlayerInstance
from src.box_container import BoxContainer
import random

class Algo1(PlayerInstance):
    def start(self):
        self.me=self._pc.get_player()
        self.nest=[]
        self.rest=[]
        self.w,self.h=self._pc.get_width(),self._pc.get_height()


        # path to nest
        self.p_nest=[ [-1 for y in range(self._pc.get_height())] for x in range(self._pc.get_width())]
        x,y=self._pc.get_nest()
        self.p_nest[x][y]=0
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

                if self.p_nest[tx][ty]==-1:
                    self.p_nest[tx][ty]=self.p_nest[curx][cury]+1
                    bfs.put((tx,ty))

        # take closest to nest
        tmp=[(x,y,self.p_nest[x][y]) for (x,y,v) in self._pc.get_ants() if v==self.me ]
        tmp.sort(key=lambda x: x[2])
        self.nest=[(x,y) for x,y,v in tmp[:4] ]
        self.rest=[(x,y) for x,y,v in tmp[4:] ]


        self.dir=((-1,-1), (1,-1), (-1,1), (1,1))
        self.neig=((-1,0), (1,0), (0,1), (0,-1))

    def run(self, kill):
        # update from last
        for i,(x,y) in enumerate(self.nest):
            move=self._pc.last_moves().get(x,y)
            if move!=None:
                self.nest[i]=move[:-1]

        for i,(x,y) in enumerate(self.rest):
            move=self._pc.last_moves().get(x,y)
            if move!=None:
                self.rest[i]=move[:-1]

        nx,ny=self._pc.get_nest()
        if self._pc.get_square(nx,ny)==self.me:
            self.rest.append((nx,ny))

        for a,d in zip(self.nest, self.dir):
            targetx,targety=nx+d[0],ny+d[1]
            x,y=a

            # it's on the position
            if x==nx+d[0] and y==ny+d[1]:
                continue

            # it's in the range
            if x>=nx-1 and x<=nx+1 and y>=ny-1 and y<=ny+1:
                if x==targetx:
                    self._pc.move(x,y,x,int(y+abs(targety-y)/(targety-y)))
                else:
                    self._pc.move(x,y,int(x+abs(targetx-x)/(targetx-x)),y)
            else:
                for neighbour in self.neig:
                    tmpx,tmpy=a[0]+neighbour[0],a[1]+neighbour[1]
                    if tmpx>=0 and tmpx<self.w and tmpy>=0 and tmpy<self.h and \
                        self.p_nest[tmpx][tmpy]!=-1 and \
                        self.p_nest[x][y]>self.p_nest[tmpx][tmpy]:
                        x,y=a[0]+neighbour[0],a[1]+neighbour[1]

                self._pc.move(a[0],a[1],x,y)

        for x,y in self.rest:
            x_new,y_new=x,y
            if random.randint(1,2)==1:
                if random.randint(1,2)==1:
                    x_new+=1
                else:
                    x_new-=1
            else:
                if random.randint(1,2)==1:
                    y_new+=1
                else:
                    y_new-=1
                        
            self._pc.move(x,y,x_new,y_new)
