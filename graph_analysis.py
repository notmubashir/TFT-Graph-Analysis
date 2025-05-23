class Node:
    def __init__(self, name, traits, cost):
        self.name = name
        self.traits = traits
        for trait in traits:
            trait.add_unit(self)
        self.cost = cost
        self.neighbors = []
        self.visited = False

    def visit(self):
        self.visited = True

    def unvisit(self):
        self.visited = False

    def get_traits(self):
        return self.traits

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def get_neighbors(self):
        return self.neighbors

    def set_neighbors(self):
        self.neighbors = []
        for trait in self.traits:
            local = trait.get_units()
            for unit in local:
                if unit != self:
                    self.neighbors.append(unit)


class Trait:
    def __init__(self, name, tiers):
        self.name = name
        self.tiers = tiers
        self.min = tiers[0]
        self.units = []

    def get_min(self):
        return self.min

    def get_name(self):
        return self.name

    def add_unit(self, unit):
        self.units.append(unit)

    def get_units(self):
        return self.units


def build_graph(unit_pool):
    for unit in unit_pool:
        unit.set_neighbors()


def add_emblem(unit, trait, unit_pool):
    unit.traits.append(trait)
    trait.add_unit(unit)
    build_graph(unit_pool)


def check_active(units, trait_pool):
    trait_pts = []
    active = []
    for unit in units:
        traits = unit.get_traits()
        for trait in traits:
            trait_pts.append(trait)
    for trait in trait_pool:
        if trait_pts.count(trait) >= trait.get_min():
            active.append([trait.get_name(), trait_pts.count(trait)])
    return active


def explore_combinations(start, path, results, visited, limit):
    path.append(start)
    visited.add(start)
    if len(path) > 1 and len(path) <= limit:
        combo = tuple(sorted(path, key=lambda x: (x.cost, x.name)))
        if combo not in results:
            results.append(combo)
    if len(path) < limit:
        for neighbor in start.get_neighbors():
            if neighbor not in visited:
                explore_combinations(neighbor, path[:], results,
                                     visited.copy(), limit)
    path.pop()
    visited.remove(start)


def explore_seeded_combinations(results, force, level):
    initial_path = force[:]
    visited = set(force)
    for node in force:
        for neighbor in node.get_neighbors():
            if neighbor not in visited:
                explore_combinations(neighbor, initial_path[:], results,
                                     visited.copy(), level)


def get_synergies(level, traits, unit_pool, trait_pool, force=[]):
    all_results = []
    if len(force) > level:
        return all_results
    if len(force) == 0:
        for unit in unit_pool:
            explore_combinations(unit, [], all_results, set(), level)
    elif len(force) == level:
        combo = tuple(sorted(force, key=lambda x: (x.cost, x.name)))
        if combo not in all_results:
            all_results.append(combo)
    else:
        explore_seeded_combinations(all_results, force, level)
    for team in all_results:
        active = check_active(team, trait_pool)
        if len(active) >= traits:
            print("Team: " + str([unit.get_name() for unit in team]) +
                  " has active traits: " + str(active))


def main():
    anima_squad = Trait('anima_squad', [3, 5, 7, 10])
    boombot = Trait('boombot', [2, 4, 6])
    cyberboss = Trait('cyberboss', [2, 3, 4])
    divinicorp = Trait('divinicorp', [1, 2, 3, 4, 5, 6, 7])
    exotech = Trait('exotech', [3, 5, 7, 10])
    nitro = Trait('nitro', [3, 4])
    golden_ox = Trait('golden_ox', [2, 4, 6])
    syndicate = Trait('syndicate', [3, 5, 7])
    street_demon = Trait('street_demon', [3, 5, 7, 10])
    cypher = Trait('cypher', [3, 4, 5])
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

    alistar = Node('alistar', [golden_ox, bruiser], 1)
    annie = Node('annie', [golden_ox, amp], 4)
    aphelios = Node('aphelios', [golden_ox, marksman], 4)
    aurora = Node('aurora', [anima_squad, dynamo], 5)
    brand = Node('brand', [street_demon, techie], 4)
    braum = Node('braum', [syndicate, vanguard], 3)
    chogath = Node('chogath', [boombot, bruiser], 4)
    darius = Node('darius', [syndicate, bruiser], 2)
    draven = Node('draven', [cypher, rapidfire], 3)
    dr_mundo = Node('dr_mundo', [street_demon, bruiser, slayer], 1)
    ekko = Node('ekko', [street_demon, strategist], 2)
    elise = Node('elise', [nitro, dynamo], 3)
    fiddlesticks = Node('fiddlesticks', [boombot, techie], 3)
    galio = Node('galio', [cypher, bastion], 3)
    garen = Node('garen', [], 5)
    gragas = Node('gragas', [divinicorp, bruiser], 3)
    graves = Node('graves', [golden_ox, executioner], 2)
    illaoi = Node('illaoi', [anima_squad, bastion], 2)
    jarvan = Node('jarvan', [golden_ox, vanguard, slayer], 3)
    jax = Node('jax', [exotech, bastion], 1)
    jhin = Node('jhin', [exotech, marksman, dynamo], 2)
    jinx = Node('jinx', [street_demon, marksman], 3)
    kindred = Node('kindred', [nitro, rapidfire, marksman], 1)
    kobuko = Node('kobuko', [cyberboss, bruiser], 5)
    kogmaw = Node('kogmaw', [boombot, rapidfire], 1)
    leblanc = Node('leblanc', [cypher, strategist], 2)
    leona = Node('leona', [anima_squad, vanguard], 4)
    miss_fortune = Node('miss_fortune', [syndicate, dynamo], 4)
    mordekaiser = Node('mordekaiser', [exotech, bruiser, techie], 3)
    morgana = Node('morgana', [divinicorp, dynamo], 1)
    naafiri = Node('naafiri', [exotech, amp], 2)
    neeko = Node('neeko', [street_demon, strategist], 4)
    nidalee = Node('nidalee', [nitro, amp], 1)
    poppy = Node('poppy', [cyberboss, bastion], 1)
    renekton = Node('renekton', [divinicorp, bastion], 5)
    rengar = Node('rengar', [street_demon, executioner], 3)
    rhaast = Node('rhaast', [divinicorp, vanguard], 2)
    samira = Node('samira', [street_demon, amp], 5)
    sejuani = Node('sejuani', [exotech, bastion], 4)
    senna = Node('senna', [divinicorp, slayer], 3)
    seraphine = Node('seraphine', [anima_squad, techie], 1)
    shaco = Node('shaco', [syndicate, slayer], 1)
    shyvana = Node('shyvana', [nitro, bastion, techie], 2)
    skarner = Node('skarner', [boombot, vanguard], 2)
    sylas = Node('sylas', [anima_squad, vanguard], 1)
    twisted_fate = Node('twisted_fate', [syndicate, rapidfire], 2)
    urgot = Node('urgot', [boombot, executioner], 5)
    varus = Node('varus', [exotech, executioner], 3)
    vayne = Node('vayne', [anima_squad, slayer], 2)
    veigar = Node('veigar', [cyberboss, techie], 2)
    vex = Node('vex', [divinicorp, executioner], 4)
    vi = Node('vi', [cypher, vanguard], 1)
    viego = Node('viego', [golden_ox, techie], 5)
    xayah = Node('xayah', [anima_squad, marksman], 4)
    yuumi = Node('yuumi', [anima_squad, amp, strategist], 3)
    zac = Node('zac', [], 5)
    zed = Node('zed', [cypher, slayer], 4)
    zeri = Node('zeri', [exotech, rapidfire], 4)
    ziggs = Node('ziggs', [cyberboss, strategist], 4)
    zyra = Node('zyra', [street_demon, techie], 1)

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

    get_synergies(7, 8, unit_pool, trait_pool, [jhin, morgana, kindred])


if __name__ == "__main__":
    main()
