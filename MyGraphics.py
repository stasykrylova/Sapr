import pylab
import matplotlib.patches as patches
import matplotlib.lines


class MyGraphics:
    def __init__(self):
        self.rod_list=[]
        self.zadelka = [] # сюда же потом нагрузки обе и моменты
        self.zadelka_code = 0
        self.nodal_loads=[]
        self.rod_loads=[]
        self.nodal_values=[]
        self.real_nodal_values=[]
        self.rod_values=[]
        self.real_rod_values=[]
        self.mashtab=[]
        self.real_width_values=[]

# Нужно подать на вход уже преобразованную длину и ширину и отступ
    def rod_init(self, coordinates, height, weight,real_width,znach):
        new_coord=[coordinates[0],coordinates[1], height,weight,znach]
        self.rod_list.append(new_coord)
        self.real_width_values.append(real_width)



    def Stopp_init(self, code):  # будет 3 варианта: 1-слева, 2-справа, 3- обе
        if code==1:
            need_rod = self.rod_list[0]
            coordinates_of_start=[need_rod[0], need_rod[1]]
            coordinates_of_end=[need_rod[0], need_rod[1]+need_rod[2]]
            self.zadelka = [coordinates_of_start, coordinates_of_end]
        elif code==2:
            need_rod = self.rod_list[-1]
            coordinates_of_start=[need_rod[0]+need_rod[3],need_rod[1]]
            coordinates_of_end=[need_rod[0]+need_rod[3],need_rod[1]+need_rod[2]]
            self.zadelka = [coordinates_of_start, coordinates_of_end]
        else:
            need_rod_first = self.rod_list[0]
            need_rod_second = self.rod_list[-1]
            coordinates_of_start_first= [need_rod_first[0], need_rod_first[1]]
            coordinates_of_end_first = [need_rod_first[0], need_rod_first[1] + need_rod_first[2]]
            coordinates_of_start_second = [need_rod_second[0] + need_rod_second[3], need_rod_second[1]]
            coordinates_of_end_second = [need_rod_second[0] + need_rod_second[3], need_rod_second[1] + need_rod_second[2]]
            self.zadelka = [coordinates_of_start_first, coordinates_of_end_first, coordinates_of_start_second, coordinates_of_end_second]

    def nodal_loads_init(self, num, value):

        if num==1:

            need_rod = self.rod_list[num - 1]
            need_load = [need_rod[0], need_rod[1]+need_rod[2]/2]
            self.nodal_loads.append(need_load)


        elif num%2==0:

            need_rod=self.rod_list[num-2]
            need_load=[need_rod[0]+need_rod[3], need_rod[1]+need_rod[2]/2]

            self.nodal_loads.append(need_load)

        else:
            need_rod = self.rod_list[num - 2]
            need_load = [need_rod[0]+need_rod[3], need_rod[1]+need_rod[2]/2]
            self.nodal_loads.append(need_load)
        self.real_nodal_values.append(value)
        if value>0:
            self.nodal_values.append(1)
        else:
            self.nodal_values.append(-1)

    def rod_loads_init(self, num, value):
        need_rod=self.rod_list[num-1]

        coord_load=[need_rod[0], need_rod[1]+need_rod[2]/2,need_rod[0]+need_rod[3], need_rod[1]+need_rod[2]/2]

        self.rod_loads.append(coord_load)
        self.real_rod_values.append(value)
        if value > 0:
            self.rod_values.append(1)
        else:
            self.rod_values.append(-1)

    def drawEverything(self, code=0, value_of_nodal_load=0, load_of_nodal_load=0, value_of_rod_load=0, rod_of_rod_load=0, znach=0):

            self.zadelka_code= code
            fig = pylab.figure()
            pylab.xlim(0, 30)
            pylab.ylim(-3, 6)
            pylab.rcParams['figure.figsize'] = [20, 20]
            # Получим текущие оси
            axes = pylab.gca()
            axes.set_aspect("equal")
            iterat=0
            for value in self.rod_list:

                indent = value[4]
                rect_coord = (value[0], value[1])
                rect_height = value[2]
                rect_width = value[3]
                rect = patches.Rectangle(rect_coord, rect_width, rect_height, edgecolor='black', facecolor='none', linewidth=3)
                axes.add_patch(rect)
                line = matplotlib.lines.Line2D([value[0], value[0]+value[3]], [value[1]-1, value[1]-1], color="black")
                line2 = matplotlib.lines.Line2D([value[0]+0.1, value[0], value[0]+0.1], [value[1]-1+0.05, value[1]-1, value[1]-1-0.05], color="black")
                line3 = matplotlib.lines.Line2D([value[0]+value[3]-0.1, value[0]+value[3], value[0]+value[3]-0.1], [value[1]-1+0.05, value[1]-1, value[1]-1-0.05], color="black")
                axes.add_line(line)
                axes.add_line(line2)
                axes.add_line(line3)
                str_len=str(self.real_width_values[iterat])
                pylab.text(value[0]+value[3]/2-len(str_len)/20, value[1]-2, str_len, horizontalalignment="center", size=15)  # "{}L".format(ДЛИНА) вместо 1 - конец+начало/2 2- низ-0.25
                #pylab.axis('off')
                iterat+=1
            if self.zadelka_code != 0:
                if self.zadelka_code == 1:
                    self.Stopp_init(1)
                    coordinates_start=self.zadelka[0]
                    coordinates_end=self.zadelka[1]
                    for y in self.frange(coordinates_start[1], coordinates_end[1], 0.2):
                        line_zadel = self.drawStopping([coordinates_start[0], coordinates_start[0]-0.2], [y, y + 0.1])
                        axes.add_line(line_zadel)
                elif self.zadelka_code == 2:
                    self.Stopp_init(2)
                    coordinates_start = self.zadelka[0]
                    coordinates_end = self.zadelka[1]
                    for y in self.frange(coordinates_start[1], coordinates_end[1], 0.2):
                        line_zadel = self.drawStopping([coordinates_start[0], coordinates_start[0]+0.2], [y , y + 0.1])

                        axes.add_line(line_zadel)
                else:
                    self.Stopp_init(3)
                    coordinates_start_first = self.zadelka[0]
                    coordinates_end_first = self.zadelka[1]
                    for y in self.frange(coordinates_start_first[1], coordinates_end_first[1], 0.2):
                        line_zadel = self.drawStopping([coordinates_start_first[0], coordinates_start_first[0] - 0.2], [y, y + 0.1])
                        axes.add_line(line_zadel)
                    coordinates_start_last = self.zadelka[2]
                    coordinates_end_last = self.zadelka[3]
                    for y in self.frange(coordinates_start_last[1], coordinates_end_last[1], 0.2):
                        line_zadel = self.drawStopping([coordinates_start_last[0], coordinates_start_last[0] + 0.2], [y, y + 0.1])

                        axes.add_line(line_zadel)
            if value_of_nodal_load!=0:
                self.nodal_loads_init(load_of_nodal_load,value_of_nodal_load)
            if len(self.nodal_loads)>0:

                i=0
                for loads in self.nodal_loads:


                    lines=self.drawNodalLoad([loads[0],loads[1]],self.nodal_values[i]/2)

                    axes.add_line(lines[0])
                    axes.add_line(lines[1])
                    str_load = str(self.real_nodal_values[i])
                    pylab.text(loads[0] + 0.2, loads[1]+0.1, str_load, horizontalalignment="center", size=10)
                    i += 1
            if value_of_rod_load!=0:
                self.rod_loads_init(rod_of_rod_load, value_of_rod_load)
            if len(self.rod_loads) > 0:
                j=0
                for rods in self.rod_loads:
                    for x in self.frange(rods[0],rods[2], 0.2):

                        lines = self.drawRodLoad([x, rods[1]], [x+0.17, rods[3]], self.rod_values[j])

                        axes.add_line(lines[0])
                        axes.add_line(lines[1])
                    str_load = str(self.real_rod_values[j])
                    pylab.text(rods[0] + rods[2]/2, rods[1] + 0.1, str_load, horizontalalignment="center", size=10)
                    j+=1


            fig.savefig('construction')
            return fig



    def drawStopping(self, start_coord, end_coord):
        line_stop = matplotlib.lines.Line2D(start_coord, end_coord, color="black")

        return line_stop

    def drawNodalLoad(self, start_coord, val):
        line_nodal_load = matplotlib.lines.Line2D([start_coord[0], start_coord[0]+val*1.5], [start_coord[1], start_coord[1]], color="black", linewidth=3)
        if val>0:
            line_nodal_load2 = matplotlib.lines.Line2D([start_coord[0]+val*1.5 - 0.2, start_coord[0]+val*1.5, start_coord[0]+val*1.5 -0.2], [start_coord[1] + 0.1, start_coord[1] , start_coord[1] - 0.1], color="black", linewidth=3)
        else:
            line_nodal_load2 = matplotlib.lines.Line2D([start_coord[0] + val*1.5 + 0.2, start_coord[0] + val*1.5, start_coord[0] + val*1.5 + 0.2],[start_coord[1] + 0.1, start_coord[1], start_coord[1] - 0.1], color="black", linewidth=3)

        return_nodals = [line_nodal_load, line_nodal_load2]
        return return_nodals

    def drawRodLoad(self, start_coord, end_coord, val):
        line_rod_load = matplotlib.lines.Line2D([start_coord[0], end_coord[0]],
                                                  [start_coord[1], end_coord[1]], color="black")
        if val > 0:
            line_rod_load2 = matplotlib.lines.Line2D([end_coord[0] - 0.1, end_coord[0], end_coord[0] - 0.1],[end_coord[1] + 0.05, end_coord[1], end_coord[1] - 0.05], color="black")
        else:
            line_rod_load2 = matplotlib.lines.Line2D(
                [start_coord[0] + 0.1, start_coord[0], start_coord[0] + 0.1],
                [start_coord[1] + 0.05, start_coord[1], start_coord[1] - 0.05], color="black")

        return_rods = [line_rod_load, line_rod_load2]
        return return_rods



    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step
