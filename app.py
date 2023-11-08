import discord
import os
import threading
from discord.ext import commands
import json
import datetime

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


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f"XP_PER_MESSAGE: {XP_PER_MESSAGE}")
    global xp_data
    xp_data = load_xp_data()
    #print('XP data loaded:', xp_data)
    print('XP data loaded')
    
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
            """AWAIT LEVEL ALGORITM OR SOMETHING (MULTIPLE FILES?)"""
            author_id = str(message.author.id) # dictionary pairs (ID -> TOTAL XP)
            xp_data.setdefault(author_id, 0) # default if it doesn't already exist
            
            xp_data[author_id] += XP_PER_MESSAGE
            print(f"{message.author} = {xp_data[author_id]}")
            #print(f"xp_data: {xp_data}")
            save_xp_data()



            try:
                if message.author.id == 811235357663297546:
                    # get level
                    guild = bot.get_guild(879548962464493619)
                    current_level = calculate_level(xp_data[author_id])
                    lvl10 = guild.get_role(1164188093713223721)
                    lvl11 = guild.get_role(1171524944354607104)
                    lvl12 = guild.get_role(1171524990257082458)
                    lvl13 = guild.get_role(1171525021928263791)
                    lvl14 = guild.get_role(1171525062201966724)
                    lvl15 = guild.get_role(1171525098465918996)
                    
                    
                    if current_level == 10:
                        if lvl10 not in message.author.roles:
                            await message.author.add_roles(lvl10)
                            print(f"Gave {message.author} {lvl10}")
                        #await message.author.remove_roles(role)

                    if current_level == 11:
                        if lvl11 not in message.author.roles:
                            await message.author.add_roles(lvl11)  
                            print(f"Gave {message.author} {lvl11}")
                            await message.author.remove_roles(lvl10)
                            print(f"Removed {lvl10} from {message.author}")
                        
                    if current_level == 12:
                        if lvl12 not in message.author.roles:
                            await message.author.add_roles(lvl12)
                            print(f"Gave {message.author} {lvl12}")
                            await message.author.remove_roles(lvl11)
                            print(f"Removed {lvl11} from {message.author}")
                            
                    if current_level == 13:
                        if lvl13 not in message.author.roles:
                            await message.author.add_roles(lvl13)
                            print(f"Gave {message.author} {lvl13}")
                            await message.author.remove_roles(lvl12)
                            print(f"Removed {lvl12} from {message.author}")
                            
                    if current_level == 14:
                        if lvl14 not in message.author.roles:
                            await message.author.add_roles(lvl14)
                            print(f"Gave {message.author} {lvl14}")
                            await message.author.remove_roles(lvl13)
                            print(f"Removed {lvl13} from {message.author}")
                            
                    if current_level == 15:
                        if lvl15 not in message.author.roles:
                            await message.author.add_roles(lvl15) 
                            print(f"Gave {message.author} {lvl15}")
                            await message.author.remove_roles(lvl14)
                            print(f"Removed {lvl14} from {message.author}")
            
            except Exception as e:
                print(f"Error: {e}")

                
            
            await bot.process_commands(message)
    except Exception as e:
        print(f"Error: {e}")

        
def calculate_level(xp):
    return int(xp ** (1.0 / 3.0))


@bot.command()
async def level(ctx):
    if ctx.author.id == 811235357663297546:

        for author_id, xp_value in xp_data.items():
            try:
                current_level = calculate_level(xp_value)
                user = bot.get_user(author_id)
                print(f"user: {user} | xp: {xp_value} | level: {current_level}") 
                
            except Exception as e:
                print(f"Error for user {author_id}: {e}")
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
