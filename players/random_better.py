from src.player_instance import PlayerInstance
from src.box_container import BoxContainer
from queue import Queue
import random

class RandomBetter(PlayerInstance):
    def start(self):
        self.me=self._pc.get_player()
        self.w,self.h=self._pc.get_width(),self._pc.get_height()
        self.block=BoxContainer(self.w, self.h)

        self.targets=((-1,-2, -1,-1),
            (+0,-2, 0,-1),
            (+1,-2, 1,-1),
            (-1,+2, -1,1),
            (+0,+2, 0,1),
            (+1,+2, 1,1),
            (-2,-1, -1,-1),
            (-2,-0, -1,0),
            (-2,+1, -1,1),
            (+2,-1, 1,-1),
            (+2,-0, 1,0),
            (+2,+1, 1,1))

        self.p_nest=self.compute_path(*self._pc.get_nest())
        self.dir=((-1,-1), (1,-1), (-1,1), (1,1))
        self.neig=((-1,0), (1,0), (0,1), (0,-1))

        # for x in self.p_nest:
            # for y in x:
                # print("{:>3}".format(y),end="")
            # print()


    def run(self, kill):
        self.block.clear()
        for x,y,a in self._pc.get_ants():
            if a==self.me:
                around=0
                x_new,y_new=x,y
                for dx in range(-1,2):
                    for dy in range(-1,2):
                        around+=self.get_ant(x+dx,y+dy, False)

                # print(around)
                if random.randint(0,around)==0:
                    # decided to move
                    maxi=self.targets[0]
                    maxv=0
                    for t in self.targets:
                        score=self.get_score(x+t[0], y+t[1])
                        if score>maxv:
                            maxv=score
                            maxi=t
                    x_new,y_new=x+maxi[2],y+maxi[3]


                    if maxv==0:
                        targetx,targety=self._pc.get_nest()
                        nx,ny=self._pc.get_nest()
                        i=random.randint(0,3)
                        targetx+=self.dir[i][0]
                        targety+=self.dir[i][1]

                        # it's in the range
                        if x>=nx-1 and x<=nx+1 and y>=ny-1 and y<=ny+1:
                            if x==targetx and y!=targety:
                                x_new,y_new=x,int(y+abs(targety-y)/(targety-y))
                            elif x!=targetx:
                                x_new,y_new=int(x+abs(targetx-x)/(targetx-x)),y
                        else:
                            bestx,besty=x,y
                            for neighbour in self.neig:
                                tmpx,tmpy=x+neighbour[0],y+neighbour[1]
                                if tmpx>=0 and tmpx<self.w and tmpy>=0 and tmpy<self.h and \
                                    self.p_nest[tmpx][tmpy]!=-1 and \
                                    self.p_nest[bestx][besty]>self.p_nest[tmpx][tmpy]:
                                        bestx,besty=tmpx,tmpy

                            x_new,y_new=bestx,besty



                # print(x,y,x_new,y_new)
                if self.block.get(x_new,y_new)==None:
                    self._pc.move(x,y,x_new,y_new)
                    self.block.insert(x_new, y_new, True)
        # print()


    def get_ant(self, x, y, me=False):
        if x<0 or x>=self.w or \
            y<0 or y>=self.h:
            return 0

        res=self._pc.get_ants().get(x,y)

        if res==-1 or res==None:
            return 0

        if (res==self.me)==me:
            return 1

        return 0

    """ return 0 if there's no ant
                min(3,1+x) where x is number of mine ants around the foe"""

    def get_score(self, x,y):
        if x<0 or x>=self.w or \
            y<0 or y>=self.h:
            return 0

        tmp=self._pc.get_ants().get(x,y)
        if tmp==None or tmp==self.me:
            return 0

        
        ants=0
        for dx in range(-1,2):
            for dy in range(-1,2):
                ants+=self.get_ant(x+dx, y+dx, True)

        return min(3, 1+ants)

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
