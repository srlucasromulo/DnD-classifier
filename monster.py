class Monster:
    def __init__(self, name, hp, exp, speed, armor, damage, elements, resistances,
                 illusionable, pushable, pushes, difficulty, occurrence,
                 paralysable, sense_invis, walk_around, walk_through):
        self.name = str(name)
        self.difficulty = int(difficulty)
        self.occurrence = int(occurrence)
        self.hp = int(hp)
        self.exp = int(exp)
        self.speed = int(speed)
        self.armor = int(armor)
        self.damage = int(damage)
        self.elements = int(elements)
        self.physical = int(resistances['Physical'])
        self.death = int(resistances['Death'])
        self.holy = int(resistances['Holy'])
        self.ice = int(resistances['Ice'])
        self.fire = int(resistances['Fire'])
        self.energy = int(resistances['Energy'])
        self.earth = int(resistances['Earth'])
        self.illusionable = int(illusionable)
        self.pushable = int(pushable)
        self.pushes = int(pushes)
        self.paralysable = int(paralysable)
        self.sense_invis = int(sense_invis)
        self.walk_around = int(walk_around)
        self.walk_through = int(walk_through)

    def __str__(self):
        string = f'{self.name},{self.difficulty},{self.occurrence},' \
                 f'{self.hp},{self.exp},{self.speed},{self.armor},{self.damage},{self.elements},' \
                 f'{self.physical},{self.death},{self.holy},{self.ice},{self.fire},{self.energy},{self.earth},' \
                 f'{self.illusionable},{self.pushable},{self.pushes},{self.paralysable},{self.sense_invis},' \
                 f'{self.walk_around},{self.walk_through}'
        return string
