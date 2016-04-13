import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter

# Uses matplotlib to display graphs in a tkinter top level (popup)
# http://www.labri.fr/perso/nrougier/teaching/matplotlib/

class PlotEvolution:

    x_limit = 0
    aggregated_avg_fitness = []
    aggregated_best_fitness = []
    aggregated_standard_deviation = []
    font = {'fontname': 'Calibri'}

    def __init__(self):
        pass

    @classmethod
    def plot_evolution(cls, avg_fitness, best_fitness, standard_deviation):

        top_level = Tkinter.Toplevel()
        figure = Figure(figsize=(9, 3), dpi=100)
        ax = figure.add_subplot(111)
        ax.set_ylim([0, 1.0])
        ax.set_ylabel("Fitness")
        ax.set_xlabel("Generations")

        generations = np.linspace(1, len(avg_fitness), len(avg_fitness), endpoint=True)

        ax.plot(generations, best_fitness, linewidth=1.5, color="red", linestyle="solid", label="Best")
        ax.plot(generations, avg_fitness, linewidth=1.5, color="green", linestyle="solid", label="Average")
        ax.plot(generations, standard_deviation, linewidth=1.5, color="blue", linestyle="solid", label="Deviation")
        ax.legend(loc='upper left', numpoints=1, prop={'size': 10})

        canvas = FigureCanvasTkAgg(figure, master=top_level)
        canvas.show()
        canvas.get_tk_widget().grid(row=0)

        toolbar = NavigationToolbar2TkAgg(canvas, top_level)
        toolbar.grid(row=1, sticky=Tkinter.W)
        toolbar.update()

        figure.tight_layout()

        top_level.mainloop()

    @classmethod
    # Receives evolution data from each step in aggregated run of EA
    def accumulate_average_data(cls, gen_avg_fitness, gen_best_fitness, gen_standard_deviation):
        cls.aggregate_avg_fitness(gen_avg_fitness)
        cls.aggregate_best_fitness(gen_best_fitness)
        cls.aggregate_standard_deviation(gen_standard_deviation)

    @classmethod
    # Clear's aggregated evolution data
    def clear_aggregated_data(cls):
        cls.aggregated_avg_fitness = []
        cls.aggregated_best_fitness = []
        cls.aggregated_standard_deviation = []

    """ Evolution Data Aggregators """

    @classmethod
    def aggregate_avg_fitness(cls, gen_avg_fitness):
        for i in xrange(len(gen_avg_fitness)):
            if i < len(cls.aggregated_avg_fitness):
                cls.aggregated_avg_fitness[i] = ((cls.aggregated_avg_fitness[i] + gen_avg_fitness[i]) / 2)
            else:
                cls.aggregated_avg_fitness.append(gen_avg_fitness[i])

    @classmethod
    def aggregate_best_fitness(cls, gen_best_fitness):
        for i in xrange(len(gen_best_fitness)):
            if i < len(cls.aggregated_best_fitness):
                cls.aggregated_best_fitness[i] = ((cls.aggregated_best_fitness[i] + gen_best_fitness[i]) / 2)
            else:
                cls.aggregated_best_fitness.append(gen_best_fitness[i])

    @classmethod
    def aggregate_standard_deviation(cls, gen_standard_deviation):
        for i in xrange(len(gen_standard_deviation)):
            if i < len(cls.aggregated_standard_deviation):
                cls.aggregated_standard_deviation[i] = ((cls.aggregated_standard_deviation[i] + gen_standard_deviation[i]) / 2)
            else:
                cls.aggregated_standard_deviation.append(gen_standard_deviation[i])
