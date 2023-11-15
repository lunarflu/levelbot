import discord
import os
import threading
from discord.ext import commands
import json
import datetime
import requests

import gradio_client
import gradio as gr
from gradio_client import Client

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix='!', intents=intents)


""""""
XP_PER_MESSAGE = 10 # 100k messages = 1M exp = lvl 100
data_file_path = '/data/xp_data.json'
xp_data = {}
""""""

API_URL = "https://api-inference.huggingface.co/models/mariagrandury/roberta-base-finetuned-sms-spam-detection"
HF_TOKEN = os.environ.get("HF_TOKEN", None)
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f"XP_PER_MESSAGE: {XP_PER_MESSAGE}")
    global xp_data
    xp_data = load_xp_data()
    #print('XP data loaded:', xp_data)
    print('XP data loaded')
    print(xp_data)
    
"""
try:
    with open('xp_data.json', 'r') as f:
        xp_data = json.load(f)
except FileNotFoundError:
    xp_data = {}

"""
    
def save_xp_data():
    with open(data_file_path, 'w') as f:
        json.dump(xp_data, f)


def load_xp_data():
    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as f:
            return json.load(f)
    return {}    


@bot.event
async def on_message(message):
    try:
        if message.author != bot.user:

            #output = query({"inputs": f"{message.content}",})
            #print(output)
            
            """AWAIT LEVEL ALGORITHM OR SOMETHING (MULTIPLE FILES?)"""
            author_id = str(message.author.id) # dictionary pairs (ID -> TOTAL XP)
            xp_data.setdefault(author_id, 0) # default if it doesn't already exist
            
            xp_data[author_id] += XP_PER_MESSAGE
            print(f"{message.author} = {xp_data[author_id]}")
            #print(f"xp_data: {xp_data}")
            save_xp_data()

            bot_ids = [1166392942387265536, 1158038249835610123, 1130774761031610388, 1155489509518098565, 1155169841276260546, 1152238037355474964, 1154395078735953930]

            try:
                if message.author.id not in bot_ids:
                    #if message.author.id == 811235357663297546:
                    # get level
                    guild = bot.get_guild(879548962464493619)
                    current_level = calculate_level(xp_data[author_id])
    
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

                    

                    lvls = {
                        1: lvl1,
                        2: lvl2,
                        3: lvl3,
                        4: lvl4,
                        5: lvl5,
                        6: lvl6,
                        7: lvl7,
                        8: lvl8,
                        9: lvl9,
                        10: lvl10,
                        11: lvl11,
                        12: lvl12,
                        13: lvl13,
                        14: lvl14,
                        15: lvl15,
                    }

                    # initial role assignment
                    if current_level == 1:
                        if lvl1 not in message.author.roles:
                            await message.author.add_roles(lvl1)
                            print(f"Gave {message.author} {lvl1}")
                    # level up
                    elif current_level >= 2 and current_level <=15:
                        current_role = lvls[current_level]
                        if current_role not in message.author.roles:
                            await message.author.add_roles(current_role)
                            print(f"Gave {message.author} {current_role}")
                            await message.author.remove_roles(lvls[current_level -1])
                            print(f"Removed {lvls[current_level -1]} from {message.author}")

            
            except Exception as e:
                print(f"Error: {e}")

            await bot.process_commands(message)
    except Exception as e:
        print(f"Error: {e}")

        
def calculate_level(xp):
    return int(xp ** (1.0 / 3.0))


def calculate_xp(level):
    return (int(level ** 3))


@bot.command()
async def restore_exp(ctx):  
    if ctx.author.id == 811235357663297546:
        try:
            guild = ctx.guild
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

            # find all members with lvl13 role
            members_with_role = [member.id for member in ctx.guild.members if lvl13 in member.roles]
            # extract user_id + xp based on level
            for member2 in members_with_role:
                print(member2)
                xp = calculate_xp(13)
                level = calculate_level(xp+1)
                print(xp)
                print(level)
                
            
        except Exception as e:
            print(f"Error: {e}")
            

@bot.command()
async def fixsheets(ctx):
    if ctx.author.id == 811235357663297546:
        try:
            # iterate through @verified role members

            # test in test sheet first

            role_id = int(900063512829755413) # 900063512829755413 = @verified
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            
            if role is None:
                print(f"Role with ID '{role_id}' not found.")
                return
        
            members_with_role = [member.id for member in ctx.guild.members if role in member.roles]
        
            print(f"Members with the role with ID '{role_id}': {', '.join(map(str, members_with_role))}")


        except Exception as e:
            print(f"Error: {e}")
            

@bot.command()
async def level(ctx):
    if ctx.author.id == 811235357663297546:

        try:
            user_data = []

            for author_id_str, xp_value in xp_data.items():
                try:
                    current_level = calculate_level(xp_value)
                    author_id = int(author_id_str)
                    user = bot.get_user(author_id)
                    user_data.append((user, xp_value, current_level))
                
                except Exception as e:
                    print(f"Error for user {author_id}: {e}")

            sorted_user_data = sorted(user_data, key=lambda x: x[1], reverse=True)

            for user, xp, level in sorted_user_data:
                print(f"user: {user} | xp: {xp} | level: {level}")

        except Exception as e:
            print(f"Error: {e}")
        """
        if author_id in xp_data:
            xp = xp_data[author_id]
            level = calculate_level(xp)
            await ctx.send(f'You are at level {level} with {xp} XP.')
        else:
            await ctx.send('You have not earned any XP yet.')
            # show top users by level / exp        
        """



@bot.command()
async def count(ctx):
    """Count total messages per user in all channels."""
    if ctx.author.id == 811235357663297546:    
        message_counts = {}
    
        for channel in ctx.guild.text_channels:
            try:
                async for message in channel.history(limit=None):
                    message_counts[message.author] = message_counts.get(message.author, 0) + 1
            except discord.Forbidden:
                # Handle the Forbidden error
                #await ctx.send(f"Missing access to read messages in {channel.name}")
                print(f"Missing access to read messages in {channel.name}")
    
        sorted_users = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)
        top_list = "\n".join([f"{member.name}: {count}" for member, count in sorted_users[:50]])
        #await ctx.send(f"Message count per user in all text channels:\n{top_list}")
        print(f"Message count per user in all text channels:\n{top_list}")


@bot.command()
async def count_messages1(ctx):
    if ctx.author.id == 811235357663297546: 
        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=1)
        message_count = 0
        for channel in ctx.guild.text_channels:
            try:
                async for message in channel.history(limit=None, after=start_date, before=end_date):
                    message_count += 1
            except discord.Forbidden:
                print(f"Missing access to read messages in {channel.name}")
        print(f'Total messages between {start_date} and {end_date}: {message_count}')


@bot.command()
async def count_messages7(ctx):
    if ctx.author.id == 811235357663297546: 
        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=7)
        message_count = 0
        for channel in ctx.guild.text_channels:
            try:
                async for message in channel.history(limit=None, after=start_date, before=end_date):
                    message_count += 1
            except discord.Forbidden:
                print(f"Missing access to read messages in {channel.name}")
        print(f'Total messages between {start_date} and {end_date}: {message_count}')


@bot.command()
async def count_messages14(ctx):
    if ctx.author.id == 811235357663297546: 
        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=14)
        message_count = 0
        for channel in ctx.guild.text_channels:
            try:
                async for message in channel.history(limit=None, after=start_date, before=end_date):
                    message_count += 1
            except discord.Forbidden:
                print(f"Missing access to read messages in {channel.name}")
        print(f'Total messages between {start_date} and {end_date}: {message_count}')  


@bot.command()
async def count_messages30(ctx):
    if ctx.author.id == 811235357663297546: 
        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=30)
        message_count = 0
        for channel in ctx.guild.text_channels:
            try:
                async for message in channel.history(limit=None, after=start_date, before=end_date):
                    message_count += 1
            except discord.Forbidden:
                print(f"Missing access to read messages in {channel.name}")
        print(f'Total messages between {start_date} and {end_date}: {message_count}')


@bot.command()
async def count_messages60(ctx):
    if ctx.author.id == 811235357663297546: 
        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=60)
        message_count = 0
        for channel in ctx.guild.text_channels:
            try:
                async for message in channel.history(limit=None, after=start_date, before=end_date):
                    message_count += 1
            except discord.Forbidden:
                print(f"Missing access to read messages in {channel.name}")
        print(f'Total messages between {start_date} and {end_date}: {message_count}')


@bot.command()
async def count_messages(ctx, time: int):
    if ctx.author.id == 811235357663297546: 
        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=time)
        message_count = 0
        for channel in ctx.guild.text_channels:
            print(channel.name)
            try:
                async for message in channel.history(limit=None, after=start_date, before=end_date):
                    message_count += 1
            except discord.Forbidden:
                print(f"Missing access to read messages in {channel.name}")
        print(f'Total messages between {start_date} and {end_date}: {message_count}')


@bot.command()
async def count_threads(ctx, time: int):
    if ctx.author.id == 811235357663297546:

        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=time)
        thread_message_count = 0
        
        for channel in ctx.guild.text_channels:
            print(f"CHANNELNAME:                      {channel.name}")
            for thread in channel.threads:
                print(channel.name)
                print(thread.name)
                async for message in thread.history(limit=None, after=start_date, before=end_date):
                    thread_message_count += 1
        print(f'Total thread_messages between {start_date} and {end_date}: {thread_message_count}')


@bot.command()
async def count_forum_threads(ctx, time: int):
    if ctx.author.id == 811235357663297546:
        end_date = datetime.datetime.utcnow()  # Current date and time
        start_date = end_date - datetime.timedelta(days=time)
        forum_thread_message_count = 0
        
        for forum in ctx.guild.forums:
            print(f"FORUMNAME:                      {forum.name}")
            for thread in forum.threads:
                print(forum.name)
                print(thread.name)
                async for message in thread.history(limit=None, after=start_date, before=end_date):
                    print(f"THREAD NAME: {thread.name}")
                    forum_thread_message_count += 1
            """
            async for thread in forum.archived_threads(limit=None, before=end_date):
                print(f"ARCHIVED THREAD NAME: {thread.name}")
                forum_thread_message_count += 1            
            """

        print(f'Total forum_thread_messages between {start_date} and {end_date}: {forum_thread_message_count}')


@bot.command()
async def top_gradio(ctx, channel_id):
    if ctx.author.id == 811235357663297546:    
        message_counts = {}
        try:
            channel = await bot.fetch_channel(channel_id)
            
            async for message in channel.history(limit=None):
                message_counts[message.author] = message_counts.get(message.author, 0) + 1
        except discord.Forbidden:
            print(f"Missing access to read messages in {channel.name}")
    
        sorted_users = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)
        top_list = "\n".join([f"{member.name}: {count}" for member, count in sorted_users[:50]])
        print(f"Message count per user in the channel:\n{top_list}")


@bot.command()
async def top_gradio_threads(ctx, channel_id):
    if ctx.author.id == 811235357663297546:    
        message_counts = {}
        
        channel = await bot.fetch_channel(channel_id)
        print(channel)
        threads = channel.threads
        print(threads)
        for thread in threads:
            print(f"Thread Name: {thread.name}, Thread ID: {thread.id}, Parent ID: {thread.parent_id}")        
            async for message in thread.history(limit=None):
                message_counts[message.author] = message_counts.get(message.author, 0) + 1
        
        async for thread in channel.archived_threads(limit=None):
            print(f"ARCHIVED Thread Name: {thread.name}, ARCHIVED Thread ID: {thread.id}, Parent ID: {thread.parent_id}") 
            async for message in thread.history(limit=None):
                message_counts[message.author] = message_counts.get(message.author, 0) + 1            



        sorted_users = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)
        top_list = "\n".join([f"[{member.id}]{member.name}: {count}" for member, count in sorted_users[:50]])
        print(f"Message count per user in the channel:\n{top_list}")

        
""""""
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
def run_bot():
    bot.run(DISCORD_TOKEN)
threading.Thread(target=run_bot).start()
def greet(name):
    return "Hello " + name + "!"
demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()    
