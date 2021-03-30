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
    await ctx.send(str(sum_dice))


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
    await ctx.send(str(sum_all))


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
bot.run(TOKEN)