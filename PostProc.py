import numpy as np
import matplotlib.pyplot as plt


class PProc:
    def __init__(self):
        print("new postproc")

    def diagram_draw(self, N_, U_):
        self.U_draw = U_
        self.N_draw = N_
        fig_N=self.pup(N_)
        fig_U=self.pup(U_)



        return [fig_N, fig_U]

    def func_draw(self,N_, U_,S_,i):
        self.N_draw=N_
        self.U_draw=U_
        self.S_draw=S_
        fig_N = self.pup([self.N_draw[i]])
        print("here is")
        fig_U = self.pup([self.U_draw[i]])
        print("here is 2")
        fig_S=self.pup([self.S_draw[i]])
        return [fig_N, fig_U,fig_S]

    def table_draw(self):
        pass


    def pup(self, X):
        clr = ['mediumorchid', 'blueviolet', 'navy', 'royalblue', 'darkslategrey', 'limegreen', 'darkgreen', 'yellow',
               'darkorange', 'orangere']
        fig, ax = plt.subplots(figsize=(5, 3))
        x = []
        y = []
        x_pred = 0
        for i in range(len(X)):
            x_ = list(X[i].keys())
            y_ = list(X[i].values())

            y.append(y_)
            x_draw = [z + x_pred for z in x_]
            x_pred = x_draw[-1]
            print(x_pred)
            print(x_draw)
            x.append(x_draw)

            ax.stackplot(x_draw, y_, labels=["here"], color=clr[i % 10])

        ax.set_xlim(xmin=x[0][0], xmax=x[-1][-1])
        fig.tight_layout()
        return fig