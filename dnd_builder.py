import numpy as np
import re

def modifier(ability_score):
    """
    return modifier value given ability score
    """
    if ability_score > 30:
        ability_score = 30
    return int(np.floor(ability_score/2)-5)

def prof_bonus(level, extra_bonus=0):
    """
    define proficiency bonus
    """
    if level > 20:
        return 6+extra_bonus
    prof = np.ceil(level/4)+1
    prof += extra_bonus
    return int(prof)

class player_character():
    """
    class to define player characters
    """
    race_dict = {'dwarf':{'constitution': 2},
                 'mountaindwarf':{'strength': 2,
                                  'constitution': 2},
                 'hilldwarf':{'constitution': 2,
                              'wisdom': 1},
                 'dragonborn':{'strength': 2,
                               'charisma': 1},
                 'elf':{'dexterity': 2},
                 'highelf':{'dexterity': 2,
                            'intelligence': 1},
                 'woodelf':{'dexterity': 2,
                            'wisdom': 1},
                 'drow':{'dexterity': 2,
                         'charisma': 1},
                 'gnome':{'intelligence': 2},
                 'forestgnome':{'dexterity': 1,
                                'intelligence': 2},
                 'rockgnome':{'constitution': 1,
                              'intelligence': 2},
                 'deepgnome':{'intelligence':2,
                              'dexterity':1},
                 'halfelf':{'charisma':2},
                 'halfling':{'dexterity': 2},
                 'lightfoothalfling':{'dexterity': 2,
                                      'charisma': 1},
                 'stouthalfling':{'dexterity': 2,
                                  'constitution': 1},
                 'halforc': {'strength': 2,
                             'constitution': 1},
                 'tiefling':{'intelligence': 1,
                             'charisma': 2},
                 'human':{'strength': 1,
                           'dexterity': 1,
                           'constitution': 1,
                           'wisdom': 1,
                           'intelligence': 1,
                           'charisma': 1},
                 'aasimar':{'charisma':2},
                 'protectoraasimar':{'charisma':2,
                                     'wisdom':1},
                 'scourgeaasimar':{'charisma':2,
                                   'constitution':1},
                 'fallenaasimar':{'charisma':2,
                                  'strength':1},
                 'firbolg':{'strength':1,
                            'wisdom':2},
                 'goliath':{'strength':2,
                            'constitution':1},
                 'kenku':{'dexterity':2,
                          'wisdom':1},
                 'lizardfolk':{'constituion':2,
                               'wisdom':1},
                 'tabaxi':{'dexterity':2,
                           'charisma':1},
                 'triton':{'strength':1,
                           'constitution':1,
                           'charisma':1},
                 'bugbear':{'strength':2,
                            'dexterity':1},
                 'hobgoblin':{'constitution':2,
                              'intelligence':1},
                 'goblin':{'dexterity':2,
                           'constitution':1},
                 'orc':{'strength':2,
                        'constitution':1,
                        'intelligence':-2},
                 'yuanti':{'charisma':2,
                           'intelligence':1},
                 'kobold':{'dexterity':2,
                           'strength':-2},
                 'centaur':{'strength':2,
                            'wisdom':1},
                 'loxodon':{'constitution':2,
                            'wisdom':1},
                 'minotaur':{'strength':2,
                             'constitution':1},
                 'simichybrid':{'constitution':2},
                 'vedalken':{'intelligence':2,
                             'wisdom':1},
                 'aarakocra':{'dexterity':2,
                              'wisdom':1},
                 'airgenasi':{'constitution':2,
                              'dexterity':1},
                 'firegenasi':{'constitution':2,
                               'intelligence':1},
                 'earthgenasi':{'constitution':2,
                                'strength':1},
                 'watergenasi':{'constitution':2,
                                'wisdom':1},
                 'beasthideshifter':{'dexterity':1,
                                     'constitution':2},
                 'longtoothshifter':{'dexterity':1,
                                     'strength':2},
                 'swiftstrideshifter':{'dexterity':2,
                                       'charisma':1},
                 'wildhuntshifter':{'dexterity':1,
                                    'wisdom':2},
                 'envoywarforged':{'constitution':1},
                 'juggernautwarforged':{'constitution':1,
                                        'strength':2},
                 'skirmisherwarforged':{'constitution':1,
                              'dexterity':2},
                 'kalashtar':{'wisdom':1,
                              'charisma':1},
                 'changling':{'charisma':2},
                 'githyanki':{'intelligence':1,
                              'strength':2},
                 'githzerai':{'intelligence':1,
                              'wisdom':2}
                 }
    
    class_health_dict = {'artificer':8,
                         'barbarian':12,
                         'bard':8,
                         'cleric':8,
                         'druid':8,
                         'fighter':10,
                         'monk':8,
                         'paladin':10,
                         'ranger':10,
                         'rogue':8,
                         'sorceror':6,
                         'warlock':8,
                         'wizard':6}
    
    class_saves_dict = {'artificer':['intelligence', 'constitution'],
                         'barbarian':['constitution', 'strength'],
                         'bard':['charisma', 'dexterity'],
                         'cleric':['wisdom', 'charisma'],
                         'druid':['wisdom', 'intelligence'],
                         'fighter':['constitution', 'strength'],
                         'monk':['strength', 'dexterity'],
                         'paladin':['charisma', 'wisdom'],
                         'ranger':['strength', 'dexterity'],
                         'rogue':['intelligence', 'dexterity'],
                         'sorceror':['charisma', 'constitution'],
                         'warlock':['charisma', 'wisdom'],
                         'wizard':['intelligence', 'wisdom']}

    def __init__(self, strength, dexterity, constitution,
                 wisdom, intelligence, charisma,
                 name, race='Human', clss = 'Barbarian',
                 level=1, rndm_health=False,
                 proficiencies=None
                 ):
        """
        initialise base character
        """
        self.race = race
        self.level = level
        self.clss = clss
        self.proficiency_bonus = self.calc_prof_bonus()
        self.name = name
        self.proficiencies = proficiencies

        self.ability_scores = {'strength': strength,
                               'dexterity': dexterity,
                               'constitution': constitution,
                               'wisdom': wisdom,
                               'intelligence': intelligence,
                               'charisma': charisma}
        self.ability_modifiers = self.calculate_ability_modifiers()

        self.racial_bonuses()
        self.update_ability_modifiers()
        
        self.hitpoints = self.define_health()
        self.max_hitpoints = self.hitpoints
                
        self.define_skills()
        #self.proficient_skills(proficiencies)

        self.initiative = self.ability_modifiers['dexterity']

        self.save_throw = self.define_saving_throw()

        self.define_spell_stats()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = f'name: {self.name}, race: {self.race}, '
        string +=f'class: {self.clss}, level: {self.level}, max hp: {self.hitpoints}\n'
        string += f'\nInitiative: {self.initiative}, proficiency bonus: {self.proficiency_bonus}\n\nAbilities:\n'
        string +=  ', '.join('%s : %s' % (k.capitalize(),self.ability_scores[k]) 
                             for k in self.ability_scores.keys())
        
        string += '\n'
        string += '\nModifiers \n'
        string +=  ', '.join('%s : %s' % (k.capitalize(),self.ability_modifiers[k]) 
                             for k in self.ability_modifiers.keys())
        
        string += '\n'
        string += '\nSaving throws: \n'
        string +=  ', '.join('%s : %s' % (k.capitalize(),self.save_throw[k]) 
                             for k in self.save_throw.keys())
        
        string += '\n'
        string += '\nSkills: \n'
        string +=  '\n'.join('%s : %s' % (k.capitalize(),self.skills[k]) 
                             for k in self.skills.keys()) 


        string += f'\n\nSpellcasting ability: {self.spell_ability}, spell save dc: {self.spell_save}, spell attack: {self.spell_attack}' 
        return string

    def calculate_ability_modifiers(self):
        """
        function to define ability modifiers
        """
        am = {}
        for key in self.ability_scores:
            am[key] = modifier(self.ability_scores[key])
        return am

    def update_ability_modifiers(self):
        """
        function to update instances
        """
        self.ability_modifiers = self.calculate_ability_modifiers()
        self.define_skills()
        self.hitpoints = self.define_health()
        self.define_spell_stats()
        

    def define_skills(self):
        """
        define skills
        """
        self.skills = {'athletics': self.ability_modifiers['strength'],
                       'acrobatics': self.ability_modifiers['dexterity'],
                       'sleight of hand': self.ability_modifiers['dexterity'],
                       'stealth': self.ability_modifiers['dexterity'],
                       'arcana': self.ability_modifiers['intelligence'],
                       'history': self.ability_modifiers['intelligence'],
                       'investigation': self.ability_modifiers['intelligence'],
                       'nature': self.ability_modifiers['intelligence'],
                       'religion': self.ability_modifiers['intelligence'],
                       'animal handling': self.ability_modifiers['wisdom'],
                       'insight': self.ability_modifiers['wisdom'],
                       'medicine': self.ability_modifiers['wisdom'],
                       'perception': self.ability_modifiers['wisdom'],
                       'survival': self.ability_modifiers['wisdom'],
                       'deception': self.ability_modifiers['charisma'],
                       'intimidation': self.ability_modifiers['charisma'],
                       'performance': self.ability_modifiers['charisma'],
                       'persuasion': self.ability_modifiers['charisma']}
        for key in self.proficiencies:
            self.skills[key.lower()] += self.proficiency_bonus

    def calc_prof_bonus(self):
        return prof_bonus(self.level)

    def racial_bonuses(self):
        # calculate racial bonuses
        act_race = self.race.lower().replace(' ', '')
        if (act_race == 'simichybrid') | (act_race == 'kalashtar'):
            print('increase one ability by 1, do this manually')
        if (act_race == 'changling'):
            print('increase dexterity or intelligence by 1, do this manually')
        if (act_race == 'envoywarforged'):
            print('increase one ability by 2, do this manually')
        if act_race not in self.race_dict:
            return
        race_bonus = self.race_dict[act_race]
        for key in race_bonus:
            self.ability_scores[key] += race_bonus[key]
            
    def add_ability_values(self, new_dict):
        """
        function to add to ability scores if required
        """
        for key in new_dict:
            self.change_ability_values(key, new_dict[key])
        self.update_ability_modifiers()
        self.define_saving_throw()
    
    def change_ability_values(self, ability, value):
        self.ability_scores[ability] += value
        self.update_ability_modifiers()
    
    def define_health(self):
        act_class = self.clss.lower()
        int_health = self.class_health_dict[act_class]
        act_race = self.race.lower().replace(' ', '')

        if act_race == 'hilldwarf':
            hp = (self.level + (int_health +
                                self.ability_modifiers['constitution'])
                  + (self.level - 1)*(int_health/2 + 1 +
                                      self.ability_modifiers['constitution'])
                 )
        else:
            hp = ((int_health +
                   self.ability_modifiers['constitution'])
                   + (self.level - 1)*(int_health/2 + 1 +
                                       self.ability_modifiers['constitution'])
                 )
        return int(hp)
    
    def define_saving_throw(self):
        self.update_ability_modifiers()
        save_throw = self.ability_modifiers.copy()
        # class benefits
        act_class = self.clss.lower()
        for save_prof in self.class_saves_dict[act_class]:
            save_throw[save_prof] += self.proficiency_bonus
        return save_throw

    def define_spell_stats(self):
        act_class = self.clss.lower()
        if (act_class == 'ranger') | (act_class == 'monk'):
            self.spell_ability = 'wisdom'
        else:
            self.spell_ability = self.class_saves_dict[act_class][0]
        
        self.spell_save = (8 + self.proficiency_bonus + 
                           self.ability_modifiers[self.spell_ability]
                          )
        
        self.spell_attack = (self.proficiency_bonus + 
                           self.ability_modifiers[self.spell_ability]
                          )