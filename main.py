# bot.py
import discord
import os
import random
from discord.ext import commands
import numpy as np
import pandas as pd

import dnd_builder as db
# from keep_alive import keep_alive

pd.set_option('display.max_colwidth', None)

# keep_alive()
description = 'dnd builder bot'
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description=description,
    help_command=commands.DefaultHelpCommand(no_category='Commands'))

spell_data = pd.read_csv('spell_list.csv')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def check_alive(ctx):
    """Checks if the bot is alive"""
    await ctx.send("I\'m alive!")


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='sum_roll', help='Simulates rolling dice and returns sum.')
async def sum_roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)]
    sum_dice = np.sum(dice)
    await ctx.send('results rolled: {}'.format(dice))
    await ctx.send('total: {}'.format(str(sum_dice)))


@bot.command(name='sum_dnd_dice',
             help='rolls any comb of dnd dice and sums them')
async def dnd_roll(ctx,
                   no_of_d20: int = 1,
                   no_of_d12: int = 0,
                   no_of_d10: int = 0,
                   no_of_d8: int = 0,
                   no_of_d6: int = 0,
                   no_of_d4: int = 0):
    if no_of_d20 > 0:
        d20_roll = [(random.choice(range(1, 21))) for x in range(no_of_d20)]
    else:
        d20_roll = [0]

    if no_of_d12 > 0:
        d12_roll = [(random.choice(range(1, 13))) for x in range(no_of_d12)]
    else:
        d12_roll = [0]

    if no_of_d10 > 0:
        d10_roll = [(random.choice(range(1, 11))) for x in range(no_of_d10)]
    else:
        d10_roll = [0]

    if no_of_d8 > 0:
        d8_roll = [(random.choice(range(1, 9))) for x in range(no_of_d8)]
    else:
        d8_roll = [0]

    if no_of_d6 > 0:
        d6_roll = [(random.choice(range(1, 7))) for x in range(no_of_d6)]
    else:
        d6_roll = [0]

    if no_of_d4 > 0:
        d4_roll = [(random.choice(range(1, 5))) for x in range(no_of_d4)]
    else:
        d4_roll = [0]
    sum_all = np.sum(
        [*d20_roll, *d12_roll, *d10_roll, *d8_roll, *d6_roll, *d4_roll])
    await ctx.send('d20 roll: {}, d12 roll: {}, d10_roll: {},'.format(d20_roll, d12_roll, d10_roll))
    await ctx.send('d8_roll: {}, d6 roll: {}, d4 roll: {}'.format(d8_roll, d6_roll, d4_roll))
    await ctx.send('total sum of dice:{}'.format(str(sum_all)))


@bot.command(name='make_char', help='make raw char using stats')
async def make_char(ctx, strength: int, dex: int, con: int, wis: int,
                    intel: int, charm: int, name: str, race: str, level: int,
                    clss: str):

    character = db.player_character(strength=strength,
                                    dexterity=dex,
                                    constitution=con,
                                    wisdom=wis,
                                    intelligence=intel,
                                    charisma=charm,
                                    name=name,
                                    race=race,
                                    level=level,
                                    clss=clss,
                                    proficiencies=[])
    filename = 'DND_{}_{}.txt'.format(clss, name.replace(' ', '_'))
    with open(filename, "w") as text_file:
        print(character, file=text_file)
    await ctx.send(str(character))
    with open(filename, "rb") as file:
        await ctx.send('\nsaved in file:', file=discord.File(file, filename))

@bot.command(name='lookup_spell',
             help='display spell information')
async def lookupspell(ctx, spell):
    spellname = spell.lower()
    spellname = spellname.replace('[^A-Za-z0-9]+', '')

    spell_sheet = spell_data[spell_data.uniq_id == spellname]

    spell_string = ('{},\nDescription: {}\nReference: {}\nRange: {}\nComponents: {}\nCasting time: {}\nRitual: {},\nDuration: {}\nConcentration: {}\nSchool: {}\nClass: {}\n Level: {}'
                    .format(str(spell_sheet['name'].iloc[0]),
                            str(spell_sheet['description'].iloc[0]),
                            str(spell_sheet['ref'].iloc[0]),
                            str(spell_sheet['range'].iloc[0]),
                            str(spell_sheet['components'].iloc[0]),
                            str(spell_sheet['cast_time'].iloc[0]),
                            str(spell_sheet['ritual'].iloc[0]),
                            str(spell_sheet['duration'].iloc[0]),
                            str(spell_sheet['concentration'].iloc[0]),
                            str(spell_sheet['school'].iloc[0]),
                            str(spell_sheet['class'].iloc[0]),
                            str(spell_sheet['level'].iloc[0]))
                    )

    await ctx.send(spell_string)

@bot.command(name='find_spell',
             help='search and display top N (default 3) spells which match keyword')
async def findspell(ctx, spell, n: int = 3):
    spellname = spell.lower()
    spellname = spellname.replace('[^A-Za-z0-9]+', '')

    spell_sheet = spell_data[spell_data.uniq_id.str.contains(spellname)]
    spell_sheet = spell_sheet.head(n)
    
    for index, row in spell_sheet.iterrows():
        spell_string = ('{},\nDescription: {}\nReference: {}\nRange: {}\nComponents: {}\nCasting time: {}\nRitual: {},\nDuration: {}\nConcentration: {}\nSchool: {}\nClass: {}\n Level: {}'
                    .format(str(row['name']),
                            str(row['description']),
                            str(row['ref']),
                            str(row['range']),
                            str(row['components']),
                            str(row['cast_time']),
                            str(row['ritual']),
                            str(row['duration']),
                            str(row['concentration']),
                            str(row['school']),
                            str(row['class']),
                            str(row['level']))
                            )
        await ctx.send(spell_string)
        await ctx.send('\n---------\n')

rec_races =  ['dwarf', 'mountaindwarf', 'hilldwarf', 'dragonborn',
              'elf', 'highelf', 'woodelf', 'drow', 'gnome', 'forestgnome',
              'rockgnome', 'deepgnome', 'halfelf', 'halfling', 
              'lightfoothalfling', 'stouthalfling', 'halforc', 'tiefling',
              'human', 'aasimar', 'protectoraasimar', 'scourgeaasimar', 
              'fallenaasimar', 'firbolg', 'goliath', 'kenku', 'lizardfolk',
              'tabaxi', 'triton', 'bugbear', 'hobgoblin', 'goblin', 'orc',
              'yuanti', 'kobold', 'centaur','loxodon','minotaur',
              'simichybrid', 'vedalken', 'aarakocra', 'airgenasi',
              'firegenasi' 'earthgenasi', 'watergenasi','beasthideshifter',
              'longtoothshifter', 'swiftstrideshifter', 'wildhuntshifter',
              'envoywarforged', 'juggernautwarforged', 'skirmisherwarforged',
              'kalashtar', 'changling', 'githyanki', 'githzerai']

rec_classes = ['artificer', 'barbarian', 'bard',
               'cleric', 'druid', 'fighter','monk',
               'paladin', 'ranger', 'rogue', 'sorceror',
               'warlock', 'wizard']

rec_skills =['athletics', 'acrobatics', 'sleight of hand',
             'stealth', 'arcana', 'history', 'investigation',
             'nature', 'religion', 'animal handling', 'insight',
             'medicine', 'perception', 'survival', 'deception',
             'intimidation', 'performance', 'persuasion']


@bot.command(name="create_char", help='guided character creation')
async def _create_char(ctx):
    # This will make sure that the response will only be registered if the following
    # conditions are met:
    await ctx.send('Hello, I will guide you through creating a character')
    await ctx.send('not you will have to have some idea and add backgrounds manually')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    await ctx.send('lets start, whats your characters name')
    nme = await bot.wait_for("message", check=check)
    name = nme.content
    return_nme = 'your name is {}'.format(name)
    await ctx.send(return_nme)

    await ctx.send('What is your race?')
    rce = await bot.wait_for('message', check = check)
    race = rce.content
    if race.lower().replace(' ', '') not in rec_races:
        await ctx.send('race not recognised, try again')
        answer1 = await bot.wait_for('message', check = check)
        answer1 = answer1.content
        if answer1.lower().replace(' ','') == 'n':
            await ctx.send('Last try:')
            race = await bot.wait_for('message', check = check, timeout=40)
            race = race.content

    # read and check the class selection
    await ctx.send('what is your class?')
    ch_clss = await bot.wait_for('message', check = check)
    ch_clss = ch_clss.content
    while ch_clss.lower() not in rec_classes:
        await ctx.send('accepted classes are')
        await ctx.send(rec_classes)
        await ctx.send('try again')
        ch_clss = await bot.wait_for('message', check = check)
        ch_clss = ch_clss.content

    # do we want to randomise stats or use standard array
    await ctx.send('do you want to randomise your initial stats (y or n)?')
    stat_method = await bot.wait_for('message', check = check)
    stat_method = stat_method.content
    if stat_method == 'y':
        avail_stats = [db.roll_random_stats() for x in range(0,6)]
        if np.sum(avail_stats) < 70:
            while np.sum(avail_stats) < 70:
                avail_stats = [db.roll_random_stats() for x in range(0,6)]
        
        await ctx.send('rolled stats are: {}'.format(avail_stats))
    else:
        await ctx.send('using standard array')
        avail_stats = [15, 14, 13, 12, 10, 8]
        await ctx.send('available stats are: {}'.format(avail_stats))
    # ------------------------------------------------------------------------
    # input ability scores from available options
    # ------------------------------------------------------------------------
    await ctx.send('Available values {}\nInput strength from available stats:\n'.format(avail_stats))
    strength = await bot.wait_for('message', check = check)
    strength = int(strength.content)
    while strength not in avail_stats:
        await ctx.send('Available values {}\nInvalid number, enter a valid number: \n'.format(avail_stats))
        strength = await bot.wait_for('message', check = check)
        strength = int(strength.content)

    avail_stats.remove(strength)

    await ctx.send('Available values {}\nInput dexterity from available stats:\n'.format(avail_stats))
    dexterity = await bot.wait_for('message', check = check)
    dexterity = int(dexterity.content)
    while dexterity not in avail_stats:
        await ctx.send('Available values {}\nInvalid number, enter a valid number: \n'.format(avail_stats))
        dexterity = await bot.wait_for('message', check = check)
        dexterity = int(dexterity.content)

    avail_stats.remove(dexterity)

    await ctx.send('Available values {}\nInput constitution from available stats:\n'.format(avail_stats))
    constitution = await bot.wait_for('message', check = check)
    constitution = int(constitution.content)
    while constitution not in avail_stats:
        await ctx.send('Available values {}\nInvalid number, enter a valid number: \n'.format(avail_stats))
        constitution = await bot.wait_for('message', check = check)
        constitution = int(constitution.content)

    avail_stats.remove(constitution)

    await ctx.send('Available values {}\nInput intelligence from available stats:\n'.format(avail_stats))
    intelligence = await bot.wait_for('message', check = check)
    intelligence = int(intelligence.content)
    while intelligence not in avail_stats:
        await ctx.send('Available values {}\nInvalid number, enter a valid number: \n'.format(avail_stats))
        intelligence = await bot.wait_for('message', check = check)
        intelligence = int(intelligence.content)

    avail_stats.remove(intelligence)

    await ctx.send('Available values {}\nInput wisdom from available stats:\n'.format(avail_stats))
    wisdom = await bot.wait_for('message', check = check)
    wisdom = int(wisdom.content)
    while wisdom not in avail_stats:
        await ctx.send('Available values {}\nInvalid number, enter a valid number: \n'.format(avail_stats))
        wisdom = await bot.wait_for('message', check = check)
        wisdom = int(wisdom.content)

    avail_stats.remove(wisdom)

    await ctx.send('Available values {}\nInput charisma from available stats:\n'.format(avail_stats))
    charisma = await bot.wait_for('message', check = check)
    charisma = int(charisma.content)
    while charisma not in avail_stats:
        await ctx.send('Available values {}\nInvalid number, enter a valid number: \n'.format(avail_stats))
        charisma = await bot.wait_for('message', check = check)
        charisma = int(charisma.content)

    avail_stats.remove(charisma)

    # input required level, may require some future options for feats and asi
    await ctx.send('what level are you?')
    level = await bot.wait_for('message', check = check)
    level = int(level.content)

    # ------------------------------------------------------------------------
    # define proficincies as final step
    # ------------------------------------------------------------------------
    message = 'finally, lets define skill proficiencies'
    message = message + '\ncheck manuals for options'
    message = message + '\naccepted skills are'
    await ctx.send(message)
    await ctx.send(rec_skills)
    await ctx.send('will stop when you enter the word stop,\nInput at least 1 and no more than 6')
    prof = []
    input_val = 'no'
    i=0
    while (input_val.lower() != 'stop') & (i<6):
        prof.append(input_val)
        await ctx.send('enter skill proficiency:')
        input_val = await bot.wait_for('message', check = check)
        input_val = input_val.content
        i += 1
        
    prof_act = [x for x in prof if x in rec_skills]
    if not prof:
        await ctx.send('no valid options given, creating defaults')
        if ch_clss.lower() in ['wizard', 'warlock', 'paladin', 'monk',
                            'cleric', 'artificier']:
            prof.append('religion')
        else:
            prof.append('perception')

    #input_ans = 'n'
    #attr_list = ['strength', 'dexterity', 'constitution',
    #             'intelligence', 'wisdom', 'charisma']
    #if level > 4:
    #    lvl_qn = '\nDo you want to increase your stats by 2? (y or n)'
    #    input_ans = input(lvl_qn)
    #    if input_ans == 'y':
    #        input_stat1 = input('which stat first?')
    #        if input_stat1.lower() not in attr_list:
    #            input_stat1 = input('input a valid stat')
    #        input_stat1 = input_stat1.lower()
    #        input_stat2 = input('which stat second?')
    #        if input_stat2.lower() not in attr_list:
    #            input_stat2 = input('input a valid stat')
    #        input_stat2 = input_stat2.lower()
    # ------------------------------------------------------------------------
    # initialise the character class
    # ------------------------------------------------------------------------
    await ctx.send('Creating your character')
    character = db.player_character(strength=strength, dexterity=dexterity, 
                                    constitution=constitution, wisdom=wisdom,
                                    intelligence=intelligence, charisma=charisma,
                                    name=name, race=race, level=level, 
                                    clss = ch_clss, proficiencies=prof_act)

    filename = 'DND_{}_{}.txt'.format(ch_clss, name.replace(' ', '_'))
    with open(filename, "w") as text_file:
        print(character, file=text_file)
    await ctx.send(str(character))
    with open(filename, "rb") as file:
        await ctx.send('\nsaved in file:', file=discord.File(file, filename))

@bot.command(name="roll_stats", help='roll random stats using Matt mercers rules')
async def _roll_stats(ctx):
    avail_stats = [db.roll_random_stats() for x in range(0,6)]
    if np.sum(avail_stats) < 70:
        while np.sum(avail_stats) < 70 & np.sum(avail_stats) > 75 :
            avail_stats = [db.roll_random_stats() for x in range(0,6)]
    await ctx.send('Rolled stats are: {}'.format(avail_stats))

bot.run(TOKEN)