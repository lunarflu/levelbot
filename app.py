import discord
import os
import threading
from discord.ext import commands
import json
import datetime
import requests
import os.path
import random
import gspread
import re


import gradio_client
import gradio as gr
from gradio_client import Client
from huggingface_hub import HfApi, list_models, list_liked_repos, list_metrics

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix='!', intents=intents)


""""""
XP_PER_MESSAGE = 10 # 100k messages = 1M exp = lvl 100
""""""
service_account = json.loads(os.environ.get('KEY'))
file_path = 'service_account.json'
with open(file_path, 'w') as json_file:
    json.dump(service_account, json_file)
gspread_bot = gspread.service_account(filename='service_account.json')
worksheet = gspread_bot.open("levelbot").sheet1
worksheet2 = gspread_bot.open("hf_discord_verified_users_test").sheet1
""""""
bot_ids = [1136614989411655780, 1166392942387265536, 1158038249835610123, 1130774761031610388, 1155489509518098565, 1155169841276260546, 1152238037355474964, 1154395078735953930]
""""""
api = HfApi()
""""""


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f"XP_PER_MESSAGE: {XP_PER_MESSAGE}")

    
def calculate_level(xp):
    return int(xp ** (1.0 / 3.0))


def calculate_xp(level):
    return (int(level ** 3))


# use a command
# check xp record presence (done in add_exp)
# check discord_user_id is verified
# do add_exp for hub?
@bot.command(name='add_exp_hub')
async def add_exp_hub(ctx):
    try:
        guild = bot.get_guild(879548962464493619)
        role = discord.utils.get(guild.roles, id=900063512829755413)
        if role:
            print(role)
            # Get members with the specified role
            """
            members_with_role = [member.id for member in guild.members if role in member.roles]
            for member_id in members_with_role:            
            """
            column_values = worksheet2.col_values(3)
            for value in column_values:
                row_number = column_values.index(value) + 1
                hf_user_name = value
                val = worksheet.acell(f'G{row_number}').value
                if val == '':
                    # check likes
                    try:
                        likes = list_liked_repos(f"{hf_user_name}")
                        hf_likes_new = likes.total
                        worksheet2.update(f'G{row_number}', f'{hf_likes_new}')
                    except Exception as e:
                        print(f"add_exp_hub Error: {e}")  
                        
    except Exception as e:
        print(f"add_exp_hub Error: {e}")  
        

async def add_exp(member_id):
    try:
        guild = bot.get_guild(879548962464493619)
        member = guild.get_member(member_id)
        lvl1 = guild.get_role(1171861537699397733)
        lvl2 = guild.get_role(1171861595115245699)
        lvl3 = guild.get_role(1171861626715115591)
        lvl4 = guild.get_role(1171861657975259206)
        lvl5 = guild.get_role(1171861686580412497)
        lvl6 = guild.get_role(1171861900301172736)
        lvl7 = guild.get_role(1171861936258941018)
        lvl8 = guild.get_role(1171861968597024868)
        lvl9 = guild.get_role(1171862009982242836)
        lvl10 = guild.get_role(1164188093713223721)
        lvl11 = guild.get_role(1171524944354607104)
        lvl12 = guild.get_role(1171524990257082458)
        lvl13 = guild.get_role(1171525021928263791)
        lvl14 = guild.get_role(1171525062201966724)
        lvl15 = guild.get_role(1171525098465918996)
        lvl16 = guild.get_role(1176826165546201099)
        lvl17 = guild.get_role(1176826221301092392)
        lvl18 = guild.get_role(1176826260643659776)
        lvl19 = guild.get_role(1176826288816791693)
        lvl20 = guild.get_role(1176826319447801896)
        lvls = {
            1: lvl1, 2: lvl2, 3: lvl3, 4: lvl4, 5: lvl5, 6: lvl6, 7: lvl7, 8: lvl8, 9: lvl9, 10: lvl10,
            11: lvl11, 12: lvl12, 13: lvl13, 14: lvl14, 15: lvl15, 16: lvl16, 17: lvl17, 18: lvl18, 19: lvl19, 20: lvl20,
        }        
        #if member.id == 811235357663297546:
        # does a record already exist?
        cell = worksheet.find(str(member.id))
        length = len(worksheet.col_values(1))
        if cell is None:
            print(f"creating new record for {member}")            
            # if not, create new record
            string_member_id = str(member.id)
            xp = 10
            current_level = calculate_level(xp)
            member_name = member.name
            worksheet.update(values=[[string_member_id, member_name, xp, current_level]], range_name=f'A{length+1}:D{length+1}')
            # initial role assignment
            if current_level == 1:
                if lvl1 not in member.roles:
                    await member.add_roles(lvl1)
                    print(f"Gave {member} {lvl1}")
        else:
            if cell:
                # if so, update that row...
                xp = worksheet.cell(cell.row, cell.col+2).value
                xp = int(xp) + XP_PER_MESSAGE
                current_level = calculate_level(xp)
                print(f"updating record for {member}: {xp} xp")
                # write with added xp
                worksheet.update(values=[[xp, current_level]], range_name=f'C{cell.row}:D{cell.row}')   
                # level up
                if current_level >= 2 and current_level <=20:
                    current_role = lvls[current_level]
                    if current_role not in member.roles:
                        await member.add_roles(current_role)
                        print(f"Gave {member} {current_role}")
                        await member.remove_roles(lvls[current_level-1])
                        print(f"Removed {lvls[current_level-1]} from {member}")  
                        print(f"{member} Level up! {[current_level-1]} -> {current_level}!")
                        #await member.send(f"Level up! {[current_level-1]} -> {current_level}!")
                        
    except Exception as e:
        print(f"add_exp Error: {e}")   


@bot.event
async def on_message(message):
    try:
        if message.author.id not in bot_ids:
            await add_exp(message.author.id)
        await bot.process_commands(message)
    except Exception as e:
        print(f"on_message Error: {e}")

        
@bot.event
async def on_reaction_add(reaction, user):
    try:
        if user.id not in bot_ids:
            await add_exp(user.id)
    except Exception as e:
        print(f"on_reaction_add Error: {e}")

        
""""""
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
def run_bot():
    bot.run(DISCORD_TOKEN)
threading.Thread(target=run_bot).start()
def greet(name):
    return "Hello " + name + "!"
demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()    
