#нужно через if подать на вход если не первый предыдуший длину и ширину м координаты конца

class Rod:
    def __init__(self, length, pl, mod_E, dopuskNapr, i, pred_end_coordinates, pred_length=0, pred_height=0,pred_height_for_draw=0):
        self.length=length
        self.area=pl
        self.elastic_modulus=mod_E
        self.allowable_stress=dopuskNapr
        self.num_rod=i
        self.num_start_node=i
        self.num_end_node=i+1
        self.pred_height_for_draw=pred_height_for_draw
        self.indent=0.0


        self.height_for_draw= pl
        self.length_for_draw=self.length


        self.indent=self.count_indent(self.area,pred_height)

        self.end_coordinates = [pred_end_coordinates[0] + self.length_for_draw, pred_end_coordinates[1]+self.indent]
        self.start_coordinates = [pred_end_coordinates[0], pred_end_coordinates[1]+self.indent]

        self.datas_for_drawing=[self.start_coordinates, self.height_for_draw, self.length_for_draw]

    def getDatas(self):
        datas={}
        datas["Length"]=self.length
        datas["Area"]= self.area
        datas["Elastic modulus"]=self.elastic_modulus
        datas["Allowable stress"]=self.allowable_stress
        return datas

    def count_height(self, height_f, height_s):
        if height_s==0:
            return 2
        elif (height_f//height_s)<1:
            return height_s-1
        else:
            return height_f//height_s

    def count_length(self, length,pred_length):
        if pred_length==0:
            return 2
        elif (length// pred_length) < 1:
            return pred_length-1
        else:
            return pred_length // length

    def count_indent(self, pl, pred_height):
        if self.num_start_node<2:

            return 0.0

        elif pl>pred_height:
            return (pred_height-pl)/2


        else:
            return (pred_height-pl)/2

    def setStop(self):
        self.stop=True




