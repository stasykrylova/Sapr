import numpy as np
from PostProc import PProc
class Counting:
    def __init__(self):
        print("New count")
        self.postp=PProc()


    def Counting_init(self, datas_json):
        self.datas_A=datas_json["Rods"]
        print("ok")
        self.datas_Delta=datas_json["Stopps"]
        self.datas_B_rods=datas_json["Rod loads"]
        self.datas_B_nodals=datas_json["Nodal loads"]


        self.datas_A_array=self.make_A_Array(self.datas_A)
        print("A:", self.datas_A_array)
        self.datas_Delta_Array=self.make_Delta_Array(self.datas_Delta, len(self.datas_A)+1)
        print("Delta: ", self.datas_Delta_Array)
        self.datas_B_Array=self.make_B_Array(self.datas_B_rods,self.datas_B_nodals,len(self.datas_A)+1 )
        print("B: ", self.datas_B_Array)
        #self.datas_for_count=self.make_datas_for_count(self.datas_A_array,self.datas_Delta_Array)
        self.datas_for_count=self.datas_A_array
        self.Count= self.MakeCount()
        print(self.Count)
        self.U_list=self.make_U()
        print("U: ", self.U_list)
        self.arr_loads = []
        self.N_list=self.make_N()
        print("N start - end :",self.N_list)
        self.N_draw_list=self.make_N_draw()
        self.U_draw_list=self.make_U_for_draw()
        self.stress=self.make_Stress()
        self.stress_arr= self.make_Stress_list()


    def make_Stress_list(self):
        s_list = []

        for i in range(len(self.U_list) - 1):
            s_rod = {}
            need_rod = self.datas_A[i + 1]
            x = 0

            while x <= (need_rod['Length'] + 0.1):
                n_x = (need_rod['Elastic modulus'] * need_rod['Area'] / need_rod['Length']) * (
                            self.U_list[i + 1] - self.U_list[i]) + ((self.arr_loads[i] * need_rod['Length']) / 2) * (
                                  1 - 2 * x / need_rod['Length'])
                s_x= n_x/need_rod['Area']
                s_rod[x] = s_x
                x += 0.1

            s_list.append(s_rod)
        print(s_list)
        return s_list


    def getDatas(self,x_):
        i=1
        L_=self.datas_A[i]["Length"]
        x=x_
        while x_>L_:
            x = x_ - L_
            L_+=self.datas_A[i]["Length"]
            i+=1

        i-=1
        need_rod=self.datas_A[i+1]
        N_=(need_rod['Elastic modulus'] * need_rod['Area'] / need_rod['Length']) *(self.U_list[i + 1] - self.U_list[i]) + ((self.arr_loads[i] * need_rod['Length']) / 2)* (1-2*x/need_rod['Length'])
        U_=self.U_list[i]+x/need_rod['Length']*(self.U_list[i+1]-self.U_list[i])+ ((self.arr_loads[i]*(need_rod['Length']**2)*x)/(2*need_rod['Elastic modulus']*need_rod['Area']*need_rod['Length']))*(1-x/need_rod['Length'])
        S_=N_/need_rod["Area"]

        return [N_,U_,S_]

    def getTable(self,i,x):
        need_rod = self.datas_A[i+1]
        print(need_rod)
        N_ = (need_rod['Elastic modulus'] * need_rod['Area'] / need_rod['Length']) * (
                    self.U_list[i + 1] - self.U_list[i]) + ((self.arr_loads[i] * need_rod['Length']) / 2) * (
                         1 - 2 * x / need_rod['Length'])
        U_ = self.U_list[i] + x / need_rod['Length'] * (self.U_list[i + 1] - self.U_list[i]) + (
                    (self.arr_loads[i] * (need_rod['Length'] ** 2) * x) / (
                        2 * need_rod['Elastic modulus'] * need_rod['Area'] * need_rod['Length'])) * (
                         1 - x / need_rod['Length'])
        S_ = N_ / need_rod["Area"]
        All_S=need_rod["Allowable stress"]
        x_str='{:.5f}'.format(x)
        N_str='{:.5f}'.format(N_)
        U_str='{:.5f}'.format(U_)
        S_str='{:.5f}'.format(S_)

        return (x_str,N_str,U_str,S_str,str(All_S))
    def makeDiagram(self):
        fig=self.postp.diagram_draw(self.N_draw_list,self.U_draw_list)
        return fig

    def makeGraf(self,i):
        fig=self.postp.func_draw(self.N_draw_list,self.U_draw_list,self.stress_arr,i)
        return fig

    def makeTable(self,i,step):
        datas=[]
        needrod=self.datas_A[i+1]
        for x_ in self.frange(0, needrod["Length"]+step, step):
            tup=self.getTable(i,x_)
            datas.append(tup)
        print("DATAS",datas)
        return datas




    def make_Stress(self):
        stress_arr=[]
        for i in self.N_list:
            arr_=[]
            for j in range(len(i)):
                need_r=self.datas_A[j+1]
                arr_.append(i[j]/need_r['Area'])
            stress_arr.append(arr_)
        print(stress_arr)
        return 0

    def make_U_for_draw(self):
        u_list=[]

        for i in range(len(self.U_list) - 1):
            u_rod={}
            need_rod=self.datas_A[i+1]
            x=0

            while x<=need_rod['Length']+0.1:
                u_x=self.U_list[i]+x/need_rod['Length']*(self.U_list[i+1]-self.U_list[i])+ ((self.arr_loads[i]*(need_rod['Length']**2)*x)/(2*need_rod['Elastic modulus']*need_rod['Area']*need_rod['Length']))*(1-x/need_rod['Length'])
                u_rod[x]=u_x
                x+=0.1
            u_list.append(u_rod)
        print(u_list)
        return u_list


    def make_N_draw(self):
        n_list = []

        for i in range(len(self.U_list) - 1):
            n_rod = {}
            need_rod = self.datas_A[i + 1]
            x = 0

            while x <= (need_rod['Length'] + 0.1):
                n_x = (need_rod['Elastic modulus'] * need_rod['Area'] / need_rod['Length']) *(self.U_list[i + 1] - self.U_list[i]) + ((self.arr_loads[i] * need_rod['Length']) / 2)* (1-2*x/need_rod['Length'])
                n_rod[x] = n_x
                x += 0.1

            n_list.append(n_rod)
        print(n_list)
        return n_list


    def make_N(self):
        N_list_start=[]
        N_list_end=[]
        print("Okay")
        for i in range(len(self.U_list)-1):
            N_list_start.append(0)
            N_list_end.append(0)
            self.arr_loads.append(0)
        for i in self.datas_B_rods:
            self.arr_loads[i-1]=self.datas_B_rods[i]


        for i in range(len(self.U_list)-1):
            need_rod= self.datas_A[i+1]

            if self.arr_loads[i]!=0:

                N_list_start[i] = (need_rod['Elastic modulus'] * need_rod['Area'] / need_rod['Length']) * (
                            self.U_list[i + 1] - self.U_list[i]) + (self.arr_loads[i]*need_rod['Length'])/2
                N_list_end[i] = N_list_start[i]-(self.arr_loads[i]*need_rod['Length'])
            else:
                N_list_start[i] = (need_rod['Elastic modulus'] * need_rod['Area'] / need_rod['Length']) * (
                        self.U_list[i + 1] - self.U_list[i])
                N_list_end[i] = N_list_start[i]



        return [N_list_start,N_list_end]


    def make_U(self):
        U_list=[]
        n=len(self.Count)
        for i in range(n):
            U_list.append(0)
        U_list[0]=self.Count[0]
        U_list[-1]=self.Count[-1]
        for i in range(n):
            U_list[i]=self.Count[i]
        return U_list



    def make_datas_for_count(self,A_, Del_):
        for i in range(len(Del_)):

            if Del_[i][0]==0:

                for j in range(len((A_))):
                    A_[j][i]=0


        return A_


    def MakeCount(self):
        for i in range(len(self.datas_Delta_Array)):
            need_= self.datas_Delta_Array[i]

            if need_[0]==0:

                self.datas_B_Array[i]=0

        a = np.array(self.datas_for_count)

        b = np.array(self.datas_B_Array)
        result = np.linalg.solve(a, b)

        return list(result.flatten())

    def make_B_Array(self, rods, nodals, len_):
        array_=[]
        for i in range(len_):
            array_.append(0)


        for i in nodals:
            array_[i-1]=nodals[i]


        for i in rods:
            need_rod=self.datas_A[i]
            array_[i-1]=array_[i-1]+need_rod['Length']/2*rods[i]
            array_[i]=array_[i]+need_rod['Length']/2*rods[i]


        return array_


    def make_Delta_Array(self, Stopping, len_):
        array_=[]
        for i in range(len_):
            array_.append([1])
        if Stopping=="Right":
            array_[-1][0]=0
        elif Stopping=="Left":
            array_[0][0]=0
        else:
            array_[0][0]=0
            array_[-1][0] = 0
        return array_


    def make_A_Array(self, array):
        array_A=[]
        n=len(array)+1
        datas=[]
        for i in range(len(array)):
            i_need=i+1
            new_arr=array[i_need]

            L_=new_arr['Length']
            A_=new_arr['Area']
            E_=new_arr['Elastic modulus']
            Stress=new_arr['Allowable stress']
            datas.append([L_,A_,E_,Stress])

        for i in range(0,n):
            array_A_small=[]
            for j in range(0,n):
                array_A_small.append(0)
            array_A.append(array_A_small)
        for i in range(0, n-1):
            need_nodal=datas[i]

            array_A[i][i]=array_A[i][i]+(need_nodal[1]*need_nodal[2])/need_nodal[0]
            array_A[i][i+1]=(-1)*(need_nodal[1]*need_nodal[2])/need_nodal[0]
            array_A[i+1][i]=(-1)*(need_nodal[1]*need_nodal[2])/need_nodal[0]
            array_A[i+1][i+1]=(need_nodal[1]*need_nodal[2])/need_nodal[0]
        if self.datas_Delta=="Right":
            for i in range(n):
                array_A[n-1][i]=0

            array_A[n-1][n-1]=1

        elif self.datas_Delta=="Left":
            for i in range(n):
                array_A[0][i]=0
            array_A[0][0]=1

        else:
            for i in range(n):

                array_A[-1][i] = 0

            array_A[-1][-1] = 1

            for i in range(n):
                array_A[0][i]=0

            array_A[0][0]=1





        return array_A


    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step


