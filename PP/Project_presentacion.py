import random
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import json
import random
#import time
import math

#Modellierung

class Node:
    
    def __init__(self,key, coordinates, infection_date, neighbors):
        
        self.key=key
        self.coordinates=coordinates
        self.infection_date=infection_date
        
        #aufsteigender Reihenfolge sortiert
        neighbors.sort()
        self.neighbors=neighbors
        
        
        #False bedeutet die Immunisierung oder dem Versterben der simulierten Person.
        self.active=True

class Virus:
    #crear nodes y meterlos a un graph.
    #graph=[obj1, obj2]
    
    def __init__(self,time,incubation_period, contageous_period, transmissibility, graph):
        #zeitpunt
        self.time=time
        
        #Zeitspanne bis zum Ausbruch der Krankheit 
        #Ein Infizierter ist für die Dauer der Krankheit ansteckend.
        self.incubation_period=incubation_period
        self.contageous_period=contageous_period
        
        #Ansteckungswahrscheinlichkeit        
        self.transmissibility=transmissibility
        
        #graph Liste von Node-Objekten, in aufsteigender Reihenfolge der Schlüssel sortiert.
        #aufsteigenden Reihenfolge der Keys 
        
        graph.sort(key=lambda x: x.key)
        self.graph=graph
        
        
        #Extra atribute: aktualizierung nach aufruf von time_step damit auch fur die 
        #visualisierung 
        
        #index der personen im graph die am anfang infektiert sind.
        self.startinfected=[]
        for i,node in enumerate(self.graph):
            if node.infection_date!=-1:
                self.startinfected.append(i)
        
        self.newinfected=set()
        self.newinmune=set()

    """ führen Sie für jeden Schlüssel k in Nd.neighbors, in aufsteigender Reihenfolge, für
    den Knoten Nd_k mit dem Schlüssel k, falls Nd_k.infection_date gleich −1 ist, das
    Folgende aus: Falls random.random() kleiner ist als self.transmissibility, dann
    setze Nd_k.infection_date auf self.time."""

    def time_step(self):
        
        self.time+=1
        
        #liste mit keys der personen/knoten.
        
        graph_keys=[]
        for elem in self.graph:
            graph_keys.append(elem.key)
    
               
        for i,node in enumerate(self.graph):
            #if person infektiert.
            if node.infection_date!=-1:
                #falls contageous_period zu ende.
                if self.time>node.infection_date + self.incubation_period + self.contageous_period:
                    #False bedeutet die Immunisierung oder den Versterben der simulierten Person.
                    node.active=False #immunisiert/tot
                    #index von neue inmmunisierte speichern 
                    self.newinmune.add(i)
                    
                #Inkubationzeit zu ende.  
                elif self.time> node.infection_date + self.incubation_period:
                    #Ausbruch der Krankheit:
                    #person kann nachbarn anstecken.
                    
                    for people in node.neighbors:
                        #speichern index der nachbarn.
                        index=graph_keys.index(people)
                        #nachbar nicht infektert:
                        if self.graph[index].infection_date==-1:
                            rd=float(random.random())
                            
                            if rd<self.transmissibility:
                                #nachbar ist infektiert, wir speichern datum der infektion.
                                self.graph[index].infection_date=self.time
                                #speichern index der neue infektierte.
                                self.newinfected.add(index)
                        

    def time_steps(self,n):
        #keys_newinfected=[]
        for i in range(n):
            self.time_step()
            
        #newinfected aktualiziert
        print(self.newinfected, "new infected")
        print(self.newinmune, " new inmune")

class VisualizeVirus:
    def __init__(self, virus):
        self.virus=virus
        #konstruire Adjazenzliste fur networkx objekt:
        #notwendig: keys und nachbarn.
        graph_visual=dict()
        for node in self.virus.graph:
            graph_visual[node.key]=set(node.neighbors)
            
        print(graph_visual)
    
        #konstruire networkx object fuer visualisirung mit Adjazenzliste. 
        self.network = nx.Graph(graph_visual)
        
        
        NETWORK_SIZE=len(virus.graph)
        
        #colors liste enthalt alle zustande der leute. grun=gesund, rot=infektiert, blau=tot od
        #zunaechst alle knoten gruen.
        self.colors = ['green'] * NETWORK_SIZE
        
        #start_infected ist eine liste mit positionen/indices 
        #i sind positionen von infektierte Leute
        for i in virus.startinfected:
            #markiere infektierte Rot!
            self.colors[i]="red"
            
            
        node_pos = nx.kamada_kawai_layout(self.network)
        
        #networkx methode fur visualierung
        nx.draw(self.network, node_color=self.colors, pos=node_pos)
        nx.draw_networkx_labels(self.network, pos=node_pos, font_color='white')
        plt.show()
        
    def Ubertragung(self,steps):
        self.virus.time_steps(steps)
        #nach jedem step werden die atributen newinfected und newinmune aktualiziert
    
        #neue infektierte werden rot markiert.
        for i in self.virus.newinfected:
            self.colors[i]= 'red' #orange

        #neue immunisierte werden blau markiert.
        for i in self.virus.newinmune:
            self.colors[i]='blue'
        
        #visualisierung
        node_pos = nx.kamada_kawai_layout(self.network)
        nx.draw(self.network, node_color=self.colors, pos=node_pos)
        nx.draw_networkx_labels(self.network, pos=node_pos, font_color='white')
        #plt.savefig(file_name + '.png')
        plt.show()
        
#konstruktion von random graph mit generate_networkx 
NETWORK_SIZE = 100

nx_g = nx.erdos_renyi_graph(NETWORK_SIZE, 0.7 * math.log(NETWORK_SIZE) / NETWORK_SIZE)

#liste mit Node objekte
list_nodes = []

#nx_node keys
for nx_node in nx_g:
    neighbors = list(nx_g.neighbors(nx_node))
    #print(neighbors)
    
    node=Node(nx_node, tuple((0,0)), -1, neighbors)    
    if random.random()< 0.05:
        #wahle personen die von anfang an infektiert sind.

        node.infection_date = 0
    list_nodes.append(node)
print(list_nodes)

#kontruktion von virus mit random graph und feste eigenschaften
virus = Virus( 0, 2, 5, 0.3, list_nodes)

#Visualize virus in zeitpunkt 0.
a=VisualizeVirus(virus)

# Visualize ansteckungen/immunisierungen nach x steps(zeit)
steps=10
a.Ubertragung(steps)


#Visualisierung virus step by step .
"""steps=1
for i in range(10):
    a.Ubertragung(steps)
    """
    


#1.beispiel Virus
"""
#true=True
#info={"time": 0, "incubation_period": 2, "contageous_period": 5, "transmissibility": 0.2, "graph": [{"key": 0, "coordinate": [0, 0], "infection_date": -1, "neighbors": [13, 32, 39], "active": true}, {"key": 1, "coordinate": [0, 0], "infection_date": -1, "neighbors": [], "active": true}, {"key": 2, "coordinate": [0, 0], "infection_date": -1, "neighbors": [16, 23, 26], "active": true}, {"key": 3, "coordinate": [0, 0], "infection_date": -1, "neighbors": [31, 38], "active": true}, {"key": 4, "coordinate": [0, 0], "infection_date": -1, "neighbors": [14], "active": true}, {"key": 5, "coordinate": [0, 0], "infection_date": -1, "neighbors": [18], "active": true}, {"key": 6, "coordinate": [0, 0], "infection_date": -1, "neighbors": [23, 32], "active": true}, {"key": 7, "coordinate": [0, 0], "infection_date": -1, "neighbors": [10, 13, 21], "active": true}, {"key": 8, "coordinate": [0, 0], "infection_date": -1, "neighbors": [9, 14, 24, 27, 36], "active": true}, {"key": 9, "coordinate": [0, 0], "infection_date": -1, "neighbors": [8, 34], "active": true}, {"key": 10, "coordinate": [0, 0], "infection_date": -1, "neighbors": [7, 25], "active": true}, {"key": 11, "coordinate": [0, 0], "infection_date": -1, "neighbors": [38], "active": true}, {"key": 12, "coordinate": [0, 0], "infection_date": -1, "neighbors": [21, 23, 35, 36], "active": true}, {"key": 13, "coordinate": [0, 0], "infection_date": -1, "neighbors": [0, 7, 25, 34], "active": true}, {"key": 14, "coordinate": [0, 0], "infection_date": -1, "neighbors": [4, 8, 16, 22], "active": true}, {"key": 15, "coordinate": [0, 0], "infection_date": -1, "neighbors": [39], "active": true}, {"key": 16, "coordinate": [0, 0], "infection_date": -1, "neighbors": [2, 14, 17, 35, 39], "active": true}, {"key": 17, "coordinate": [0, 0], "infection_date": -1, "neighbors": [16], "active": true}, {"key": 18, "coordinate": [0, 0], "infection_date": -1, "neighbors": [5, 22], "active": true}, {"key": 19, "coordinate": [0, 0], "infection_date": -1, "neighbors": [], "active": true}, {"key": 20, "coordinate": [0, 0], "infection_date": -1, "neighbors": [21, 33, 39], "active": true}, {"key": 21, "coordinate": [0, 0], "infection_date": 0, "neighbors": [7, 12, 20], "active": true}, {"key": 22, "coordinate": [0, 0], "infection_date": -1, "neighbors": [14, 18, 27], "active": true}, {"key": 23, "coordinate": [0, 0], "infection_date": -1, "neighbors": [2, 6, 12, 30, 36], "active": true}, {"key": 24, "coordinate": [0, 0], "infection_date": -1, "neighbors": [8, 37], "active": true}, {"key": 25, "coordinate": [0, 0], "infection_date": -1, "neighbors": [10, 13], "active": true}, {"key": 26, "coordinate": [0, 0], "infection_date": -1, "neighbors": [2, 37], "active": true}, {"key": 27, "coordinate": [0, 0], "infection_date": -1, "neighbors": [8, 22], "active": true}, {"key": 28, "coordinate": [0, 0], "infection_date": -1, "neighbors": [32], "active": true}, {"key": 29, "coordinate": [0, 0], "infection_date": -1, "neighbors": [36, 38], "active": true}, {"key": 30, "coordinate": [0, 0], "infection_date": -1, "neighbors": [23, 37, 39], "active": true}, {"key": 31, "coordinate": [0, 0], "infection_date": -1, "neighbors": [3], "active": true}, {"key": 32, "coordinate": [0, 0], "infection_date": -1, "neighbors": [0, 6, 28], "active": true}, {"key": 33, "coordinate": [0, 0], "infection_date": -1, "neighbors": [20], "active": true}, {"key": 34, "coordinate": [0, 0], "infection_date": -1, "neighbors": [9, 13], "active": true}, {"key": 35, "coordinate": [0, 0], "infection_date": -1, "neighbors": [12, 16, 36], "active": true}, {"key": 36, "coordinate": [0, 0], "infection_date": -1, "neighbors": [8, 12, 23, 29, 35], "active": true}, {"key": 37, "coordinate": [0, 0], "infection_date": -1, "neighbors": [24, 26, 30], "active": true}, {"key": 38, "coordinate": [0, 0], "infection_date": -1, "neighbors": [3, 11, 29], "active": true}, {"key": 39, "coordinate": [0, 0], "infection_date": -1, "neighbors": [0, 15, 16, 20, 30], "active": true}]}
    

graph=info["graph"]
time=info["time"]
transmissibility=info["transmissibility"]
contageous_period=info["contageous_period"]
incubation_period=info["incubation_period"]   
new_graph=[]    

for dic in graph:
    #new_graph.append(node(dic["key"],dic["coordinate"], dic["infection_date"],dic["neighbors"], dic["active"]))
    new_graph.append(Node(dic["key"],dic["coordinate"], dic["infection_date"],dic["neighbors"]))

       
virus=Virus(time,incubation_period, contageous_period, transmissibility, new_graph)

"""
#Virus={'time': 0, 'incubation_period': 2, 'contageous_period': 5, 'transmissibility': 0.2, 'graph': [{'key': 0, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [1], 'active': True}, {'key': 1, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [0, 5, 6], 'active': True}, {'key': 2, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [], 'active': True}, {'key': 3, 'coordinate': (0, 0), 'infection_date': 0, 'neighbors': [], 'active': True}, {'key': 4, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [], 'active': True}, {'key': 5, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [1, 9], 'active': True}, {'key': 6, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [1], 'active': True}, {'key': 7, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [], 'active': True}, {'key': 8, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [], 'active': True}, {'key': 9, 'coordinate': (0, 0), 'infection_date': -1, 'neighbors': [5], 'active': True}]}
#create object Virus with all his functions