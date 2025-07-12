import itertools
from collections import Counter
import time


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


def trait_potential(comp, comp_size, trait_pool):
    trait_counts = Counter()
    for trait in trait_pool:
        trait_counts[trait] = 0
    for unit in comp:
        for trait in unit.get_traits():
            trait_counts[trait] += 1
    remaining_slots = comp_size - len(comp)
    current_traits = 0
    possible_traits = 0
    for trait, current_count in trait_counts.items():
        if current_count >= trait.get_min():
            current_traits += 1
        elif current_count + remaining_slots >= trait.get_min():
            possible_traits += 1
    return current_traits, possible_traits


def check_active(units):
    trait_counts = Counter()
    active = Counter()
    for unit in units:
        traits = unit.get_traits()
        for trait in traits:
            trait_counts[trait] += 1
    for trait in trait_counts:
        if trait_counts[trait] >= trait.get_min():
            active[trait.get_name()] = trait_counts[trait]
    return active


def iterate_seeded_growth(comp_pool):
    results = []
    excluded = []
    prev_seed = None
    for team in comp_pool:
        neighbors = []
        current_seed = team[0]
        if current_seed != prev_seed and prev_seed is not None:
            excluded.append(prev_seed)
        for node in team:
            for neighbor in node.get_neighbors():
                if neighbor not in team and neighbor not in neighbors:
                    if neighbor not in excluded:
                        neighbors.append(neighbor)
        for neighbor in neighbors:
            sorted_team = tuple(sorted(team + (neighbor,), key=lambda x:
                                       (x.cost, x.name)))
            if sorted_team not in results:
                results.append(sorted_team)
        prev_seed = current_seed
    sorted_results = list(sorted(results, key=lambda x: (x[0].cost,
                                                         x[0].name)))
    return sorted_results


def flatten_once(seq):
    for item in seq:
        if isinstance(item, tuple):
            yield from item
        else:
            yield item


def print_timer(end, start):
    print("         Took " + str(end - start) + " seconds to complete.")


def get_hybrid(split, unit_pool, trait_pool, force=[]):
    start_time = time.time()

    branches_2 = []
    branches_3 = []
    branches_4 = []

    units = [tuple([unit]) for unit in unit_pool]
    if 2 in split or 3 in split or 4 in split:
        branches_2 = iterate_seeded_growth(units)
        if 3 in split or 4 in split:
            branches_3 = iterate_seeded_growth(branches_2)
            if 4 in split:
                branches_4 = iterate_seeded_growth(branches_3)

    for branch in branches_2:
        current, potential = trait_potential(branch, 3, trait_pool)
        if current < 2 and potential < 3:
            branches_2.remove(branch)
    for branch in branches_3:
        current, potential = trait_potential(branch, 4, trait_pool)
        if current < 3 and potential < 4:
            branches_3.remove(branch)
    for branch in branches_4:
        current, potential = trait_potential(branch, 5, trait_pool)
        if current < 4 and potential < 5:
            branches_4.remove(branch)

    ones = itertools.combinations(unit_pool, split.count(1))
    twos = itertools.combinations(branches_2, split.count(2))
    threes = itertools.combinations(branches_3, split.count(3))
    fours = itertools.combinations(branches_4, split.count(4))

    final_comps = itertools.product(fours, threes, twos, ones)
    unwraps = 1
    if len(force) > 0:
        final_comps = itertools.product(final_comps, [tuple(force)])
        unwraps += 1

    end_time = time.time()
    print('Gathered combinations of splits ' + str(split) + ":")
    print_timer(end_time, start_time)

    return final_comps


def get_branches(level, unit_pool, force=[]):
    start_time = time.time()
    final_comps = force
    if len(force) > level:
        return []
    if len(force) < level:
        if len(force) > 0:
            final_comps = iterate_seeded_growth([force])
        else:
            final_comps = [tuple([unit]) for unit in unit_pool]
        for _ in range(level - len(force) - 1):
            final_comps = iterate_seeded_growth(final_comps)

    end_time = time.time()
    print('Traversed branches of length ' + str(level) + ":")
    print_timer(end_time, start_time)

    return final_comps


def get_combinations(level, unit_pool, force=[]):
    start_time = time.time()

    final_comps = []
    if len(force) < level:
        final_comps = itertools.combinations(unit_pool, level - len(force))
    if len(force) > 0:
        final_comps = itertools.product(final_comps, [force])

    end_time = time.time()
    print('Generated combinations of length ' + str(level) + ":")
    print_timer(end_time, start_time)

    return final_comps


def validate(comps, level, traits, unwraps=0):
    start_time = time.time()

    seen = set()
    unique_comps = []
    all_comps = 0
    validated_comps = 0

    for team in comps:
        all_comps += 1
        flattened_team = team
        for _ in range(unwraps):
            flattened_team = flatten_once(flattened_team)
        flattened_team = set(flattened_team)
        if len(flattened_team) == level:
            sorted_team_key = tuple(sorted((unit.cost, unit.name)
                                           for unit in flattened_team))
            if sorted_team_key not in seen:
                active = check_active(flattened_team)
                if len(active) >= traits:
                    seen.add(sorted_team_key)
                    unique_comps.append((flattened_team))
                    validated_comps += 1

    end_time = time.time()
    print('Validated ' + str(validated_comps) + ' comps out of ' +
          str(all_comps) + ':')
    print_timer(end_time, start_time)

    return unique_comps


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

    trait_pool = [anima_squad, boombot, cyberboss, divinicorp, exotech,
                  nitro, golden_ox, syndicate, street_demon, cypher, bastion,
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

    """
    units = [tuple([unit]) for unit in unit_pool]
    branches_2 = iterate_seeded_growth(units)
    branches_3 = iterate_seeded_growth(branches_2)
    branches_4 = iterate_seeded_growth(branches_3)

    print('branches_2: ' + str(len(branches_2)))
    for branch in branches_2:
        current, potential = trait_potential(branch, 3, trait_pool)
        if current < 2 and potential < 3:
            branches_2.remove(branch)
    print('filtered branches_2: ' + str(len(branches_2)))
    print('branches_3: ' + str(len(branches_3)))
    for branch in branches_3:
        current, potential = trait_potential(branch, 4, trait_pool)
        if current < 3 and potential < 4:
            branches_3.remove(branch)
    print('filtered branches_3: ' + str(len(branches_3)))
    print('branches_4: ' + str(len(branches_4)))
    for branch in branches_4:
        current, potential = trait_potential(branch, 5, trait_pool)
        if current < 4 and potential < 5:
            branches_4.remove(branch)
    print('filtered branches_4: ' + str(len(branches_4)))
    """

    validate(get_hybrid([2, 2, 1], unit_pool, trait_pool, []), 5, 5, 2)


if __name__ == "__main__":
    main()
