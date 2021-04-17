from manim import *
import numpy as np
import pymongo

mongo_url = "mongodb+srv://javitau:UkQqHDSmyscRVl6C@cluster0.38tql.mongodb.net/shellxactas?retryWrites=true&w=majority" #os.getenv('MONGO_URL')
mongoclient = pymongo.MongoClient(mongo_url)
mongoprueba = mongoclient['Shellxactas']
mongocampus = mongoprueba['campus']

times = []
for i in mongocampus.find({},{'_id': 0, 'times': 1}):
    times.append(i['times'])

class CampusPlot(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            x_min=0,
            x_max=len(times)-1,
            y_min=0,
            x_axis_config={"tick_frequency": 10},
            y_axis_config={"tick_frequency": 10},
            y_labeled_nums= np.arange(0, max(times), 10),
            y_max=max(times),
            **kwargs
        )
    def construct(self):
        self.setup_axes(animate=True)
        times_graph = self.get_graph(lambda x: times[int(x)], color=RED)
        times_text = Text("Cant. de caidas", color=RED)
        times_text.to_corner(UR)
        mean_graph = self.get_graph(lambda x: np.mean(times[:int(x)+1]), color=BLUE)
        mean_text = Text("Promedio", color=BLUE).next_to(times_text, DOWN)
        self.play(Create(times_graph), Create(times_text), Create(mean_graph), Create(mean_text), run_time = 7)
        self.wait(1)