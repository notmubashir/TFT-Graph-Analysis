import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, name, traits, cost):
        self.name = name
        self.traits = traits
        if len(traits) > 0:
            self.color = traits[0].get_color()
        else:
            self.color = '#a2a2a2'
        for trait in traits:
            trait.add_unit(self)
        self.cost = cost
        self.neighbors = []

    def get_traits(self):
        return self.traits

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def get_neighbors(self):
        return self.neighbors

    def get_color(self):
        return self.color

    def set_neighbors(self):
        self.neighbors = []
        for trait in self.traits:
            local = trait.get_units()
            for unit in local:
                if unit != self:
                    self.neighbors.append(unit)


class Trait:
    def __init__(self, name, tiers, color='#a2a2a2'):
        self.name = name
        self.tiers = tiers
        self.min = tiers[0]
        self.units = []
        self.color = color

    def get_min(self):
        return self.min

    def get_name(self):
        return self.name

    def add_unit(self, unit):
        self.units.append(unit)

    def get_units(self):
        return self.units

    def get_color(self):
        return self.color


class GraphVisualization:
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.disconnected_pos = {}

    def addEdge(self, a, b):
        temp = [a, b]
        self.edges.append(temp)

    def addNode(self, a, pos):
        self.nodes.append(a)
        self.disconnected_pos[a] = pos

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        pos = nx.kamada_kawai_layout(G)
        G.add_nodes_from(self.nodes)
        for node in self.nodes:
            pos[node] = self.disconnected_pos[node]
        colormap = []
        labels = {}
        for node in G:
            colormap.append(node.get_color())
            labels[node] = node.get_name()
        nx.draw(G, pos=pos, ax=None, with_labels=True, font_size=8,
                node_size=1000, node_color=colormap, labels=labels)
        plt.show()


def build_graph(unit_pool):
    for unit in unit_pool:
        unit.set_neighbors()


def add_emblem(unit, trait, unit_pool):
    unit.traits.append(trait)
    trait.add_unit(unit)
    build_graph(unit_pool)


def main():
    anima_squad = Trait('anima_squad', [3, 5, 7, 10], '#ffaaf7')
    boombot = Trait('boombot', [2, 4, 6], "#ad620c")
    cyberboss = Trait('cyberboss', [2, 3, 4], "#5964f3")
    divinicorp = Trait('divinicorp', [1, 2, 3, 4, 5, 6, 7], "#8ed5ff")
    exotech = Trait('exotech', [3, 5, 7, 10], "#676A77")
    nitro = Trait('nitro', [3, 4], "#f03629")
    golden_ox = Trait('golden_ox', [2, 4, 6], "#ffd000")
    syndicate = Trait('syndicate', [3, 5, 7], "#8547cc")
    street_demon = Trait('street_demon', [3, 5, 7, 10], "#00ffc8")
    cypher = Trait('cypher', [3, 4, 5], "#66ff00")
    bastion = Trait('bastion', [2, 4, 6])
    bruiser = Trait('bruiser', [2, 4, 6])
    strategist = Trait('strategist', [2, 3, 4, 5])
    executioner = Trait('executioner', [2, 3, 4, 5])
    marksman = Trait('marksman', [2, 4])
    slayer = Trait('slayer', [2, 4, 6])
    amp = Trait('amp', [2, 3, 4, 5])
    rapidfire = Trait('rapidfire', [2, 4, 6])
    techie = Trait('techie', [2, 4, 6, 8])
    dynamo = Trait('dynamo', [2, 3, 4])
    vanguard = Trait('vanguard', [2, 4, 6])

    trait_pool = [anima_squad, boombot, cyberboss, divinicorp, exotech, nitro,
                  golden_ox, syndicate, street_demon, cypher, bastion,
                  bruiser, strategist, executioner, marksman, slayer, amp,
                  rapidfire, techie, dynamo, vanguard]

    alistar = Node('Alistar', [golden_ox, bruiser], 1)
    annie = Node('Annie', [golden_ox, amp], 4)
    aphelios = Node('Aphelios', [golden_ox, marksman], 4)
    aurora = Node('Aurora', [anima_squad, dynamo], 5)
    brand = Node('Brand', [street_demon, techie], 4)
    braum = Node('Braum', [syndicate, vanguard], 3)
    chogath = Node('Chogath', [boombot, bruiser], 4)
    darius = Node('Darius', [syndicate, bruiser], 2)
    draven = Node('Draven', [cypher, rapidfire], 3)
    dr_mundo = Node('Dr. Mundo', [street_demon, bruiser, slayer], 1)
    ekko = Node('Ekko', [street_demon, strategist], 2)
    elise = Node('Elise', [nitro, dynamo], 3)
    fiddlesticks = Node('Fiddlesticks', [boombot, techie], 3)
    galio = Node('Galio', [cypher, bastion], 3)
    garen = Node('Garen', [], 5)
    gragas = Node('Gragas', [divinicorp, bruiser], 3)
    graves = Node('Graves', [golden_ox, executioner], 2)
    illaoi = Node('Illaoi', [anima_squad, bastion], 2)
    jarvan = Node('Jarvan IV', [golden_ox, vanguard, slayer], 3)
    jax = Node('Jax', [exotech, bastion], 1)
    jhin = Node('Jhin', [exotech, marksman, dynamo], 2)
    jinx = Node('Jinx', [street_demon, marksman], 3)
    kindred = Node('Kindred', [nitro, rapidfire, marksman], 1)
    kobuko = Node('Kobuko', [cyberboss, bruiser], 5)
    kogmaw = Node("Kog'Maw", [boombot, rapidfire], 1)
    leblanc = Node('LeBlanc', [cypher, strategist], 2)
    leona = Node('Leona', [anima_squad, vanguard], 4)
    miss_fortune = Node('Miss Fortune', [syndicate, dynamo], 4)
    mordekaiser = Node('Mordekaiser', [exotech, bruiser, techie], 3)
    morgana = Node('Morgana', [divinicorp, dynamo], 1)
    naafiri = Node('Naafiri', [exotech, amp], 2)
    neeko = Node('Neeko', [street_demon, strategist], 4)
    nidalee = Node('Nidalee', [nitro, amp], 1)
    poppy = Node('Poppy', [cyberboss, bastion], 1)
    renekton = Node('Renekton', [divinicorp, bastion], 5)
    rengar = Node('Rengar', [street_demon, executioner], 3)
    rhaast = Node('Rhaast', [divinicorp, vanguard], 2)
    samira = Node('Samira', [street_demon, amp], 5)
    sejuani = Node('Sejuani', [exotech, bastion], 4)
    senna = Node('Senna', [divinicorp, slayer], 3)
    seraphine = Node('Seraphine', [anima_squad, techie], 1)
    shaco = Node('Shaco', [syndicate, slayer], 1)
    shyvana = Node('Shyvana', [nitro, bastion, techie], 2)
    skarner = Node('Skarner', [boombot, vanguard], 2)
    sylas = Node('Sylas', [anima_squad, vanguard], 1)
    twisted_fate = Node('Twisted Fate', [syndicate, rapidfire], 2)
    urgot = Node('Urgot', [boombot, executioner], 5)
    varus = Node('Varus', [exotech, executioner], 3)
    vayne = Node('Vayne', [anima_squad, slayer], 2)
    veigar = Node('Veigar', [cyberboss, techie], 2)
    vex = Node('Vex', [divinicorp, executioner], 4)
    vi = Node('Vi', [cypher, vanguard], 1)
    viego = Node('Viego', [golden_ox, techie], 5)
    xayah = Node('Xayah', [anima_squad, marksman], 4)
    yuumi = Node('Yuumi', [anima_squad, amp, strategist], 3)
    zac = Node('Zac', [], 5)
    zed = Node('Zed', [cypher, slayer], 4)
    zeri = Node('Zeri', [exotech, rapidfire], 4)
    ziggs = Node('Ziggs', [cyberboss, strategist], 4)
    zyra = Node('Zyra', [street_demon, techie], 1)

    unit_pool = [alistar, annie, aphelios, aurora, brand, braum, chogath,
                 darius, draven, dr_mundo, ekko, elise, fiddlesticks, galio,
                 garen, gragas, graves, illaoi, jarvan, jax, jhin, jinx,
                 kindred, kobuko, kogmaw, leblanc, leona, miss_fortune,
                 mordekaiser, morgana, naafiri, neeko, nidalee, poppy,
                 renekton, rengar, rhaast, samira, sejuani, senna, seraphine,
                 shaco, shyvana, skarner, sylas, twisted_fate, urgot, varus,
                 vayne, veigar, vex, vi, viego, xayah, yuumi, zac, zed, zeri,
                 ziggs, zyra]

    build_graph(unit_pool)

    unit_graph = GraphVisualization()
    plotted = []
    for unit in unit_pool:
        for neighbor in unit.get_neighbors():
            if neighbor not in plotted:
                unit_graph.addEdge(unit, neighbor)
        if unit is garen:
            unit_graph.addNode(unit, [0.75, 0.75])
        if unit is zac:
            unit_graph.addNode(unit, [0.75, -0.75])
        plotted.append(unit)
    unit_graph.visualize()


if __name__ == "__main__":
    main()
