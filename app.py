import discord
import os
import threading
from discord.ext import commands
import json
import datetime
import requests
import os.path
import gspread

import gradio_client
import gradio as gr
from gradio_client import Client

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix='!', intents=intents)


""""""
XP_PER_MESSAGE = 10 # 100k messages = 1M exp = lvl 100
#data_file_path = '/data/xp_data.json'
#xp_data = {}
""""""
service_account = json.loads(os.environ.get('KEY'))
file_path = 'service_account.json'
with open(file_path, 'w') as json_file:
    json.dump(service_account, json_file)
gspread_bot = gspread.service_account(filename='service_account.json')
worksheet = gspread_bot.open("levelbot").sheet1
""""""
API_URL = "https://api-inference.huggingface.co/models/mariagrandury/roberta-base-finetuned-sms-spam-detection"
HF_TOKEN = os.environ.get("HF_TOKEN", None)
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
""""""

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f"XP_PER_MESSAGE: {XP_PER_MESSAGE}")


def calculate_level(xp):
    return int(xp ** (1.0 / 3.0))


def calculate_xp(level):
    return (int(level ** 3))


@bot.event
async def on_message(message):
    try:
        if message.author != bot.user:

            #output = query({"inputs": f"{message.content}",})
            #print(output)
            bot_ids = [1166392942387265536, 1158038249835610123, 1130774761031610388, 1155489509518098565, 1155169841276260546, 1152238037355474964, 1154395078735953930]

            try:
                if message.author.id not in bot_ids:
                    #if message.author.id == 811235357663297546:
                    # get level
                    guild = bot.get_guild(879548962464493619)
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
        
                    # does a record already exist?
                    cell = worksheet.find(str(message.author.id))
                    length = len(worksheet.col_values(1))
                    if cell is None:
                        print(f"creating new record for {member}")            
                        # if not, create new record
                        xp = 10
                        worksheet.update(values=[[string_member_id, member.name, xp, level]], range_name=f'A{length+1}:D{length+1}')
                    else:
                        if cell:
                            print(f"updating record for {member}")
                            # if so, update that row...
                            # update exp, can only be in a positive direction
                            # read
                            xp = worksheet.cell(cell.row, cell.col+2).value
                            xp += XP_PER_MESSAGE
                            current_level = calculate_level(xp)
                            # write with added xp
                            worksheet.update(values=[[xp, current_level]], range_name=f'C{cell.row}:D{cell.row}')   

                            if current_level == 2:
                                if lvl2 not in message.author.roles:
                                    await message.author.add_roles(lvl2)  
                                    print(f"Gave {message.author} {lvl2}")
                                    await message.author.remove_roles(lvl1)
                                    print(f"Removed {lvl1} from {message.author}")
            
                            if current_level == 3:
                                if lvl3 not in message.author.roles:
                                    await message.author.add_roles(lvl3)  
                                    print(f"Gave {message.author} {lvl3}")
                                    await message.author.remove_roles(lvl2)
                                    print(f"Removed {lvl2} from {message.author}")
            
                            if current_level == 4:
                                if lvl4 not in message.author.roles:
                                    await message.author.add_roles(lvl4)  
                                    print(f"Gave {message.author} {lvl4}")
                                    await message.author.remove_roles(lvl3)
                                    print(f"Removed {lvl3} from {message.author}")
            
                            if current_level == 5:
                                if lvl5 not in message.author.roles:
                                    await message.author.add_roles(lvl5)  
                                    print(f"Gave {message.author} {lvl5}")
                                    await message.author.remove_roles(lvl4)
                                    print(f"Removed {lvl4} from {message.author}")
            
                            if current_level == 6:
                                if lvl6 not in message.author.roles:
                                    await message.author.add_roles(lvl6)  
                                    print(f"Gave {message.author} {lvl6}")
                                    await message.author.remove_roles(lvl5)
                                    print(f"Removed {lvl5} from {message.author}")
                                    
                            if current_level == 7:
                                if lvl7 not in message.author.roles:
                                    await message.author.add_roles(lvl7)  
                                    print(f"Gave {message.author} {lvl7}")
                                    await message.author.remove_roles(lvl6)
                                    print(f"Removed {lvl6} from {message.author}")
            
                            if current_level == 8:
                                if lvl8 not in message.author.roles:
                                    await message.author.add_roles(lvl8)  
                                    print(f"Gave {message.author} {lvl8}")
                                    await message.author.remove_roles(lvl7)
                                    print(f"Removed {lvl7} from {message.author}")
                            
                            if current_level == 9:
                                if lvl9 not in message.author.roles:
                                    await message.author.add_roles(lvl9)  
                                    print(f"Gave {message.author} {lvl9}")
                                    await message.author.remove_roles(lvl8)
                                    print(f"Removed {lvl8} from {message.author}")                    
                            
                            if current_level == 10:
                                if lvl10 not in message.author.roles:
                                    await message.author.add_roles(lvl10)
                                    print(f"Gave {message.author} {lvl10}")
                                    await message.author.remove_roles(lvl9)
                                    print(f"Removed {lvl9} from {message.author}") 
            
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

        
                            """
                            value = cell.value
                            row_number = cell.row
                            column_number = cell.col                
                            """                    

            
            except Exception as e:
                print(f"Error: {e}")

            await bot.process_commands(message)
            
    except Exception as e:
        print(f"Error: {e}")

        



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


            level_roles = [lvl1,lvl2,lvl3,lvl4,lvl5,lvl6,lvl7,lvl8,lvl9,lvl10,lvl11,lvl12,lvl13,lvl14,lvl15]
            
            member_id_column_values = worksheet.col_values(1)

            for role in level_roles:
                role_members = [member.id for member in ctx.guild.members if role in member.roles]
            
                # role = position in level_roles + some adjustment factor
                # list of people in a given role (e.g. lvl5)
                print(f"role: {role} | role_members: {role_members}")
                
                #members_with_role = [member.id for member in ctx.guild.members if lvl13 in member.roles]
                # extract user_id + xp based on level
                for member_id in role_members:
                    string_member_id = str(member_id)
                    if string_member_id in member_id_column_values:
                        continue
                    
                    member = await bot.fetch_user(member_id)
                    #xp = calculate_xp(13)
                    position = level_roles.index(role) + 1
                    xp = calculate_xp(position)
                    level = calculate_level(xp+1)
                    print(f"{role} {level} {xp} {member}")
                    
                    string_xp = str(xp)
                    string_level = str(level)
                    
                    # get column name / data to safetycheck
    
                    
                    # does a record already exist?
                    cell = worksheet.find(string_member_id)

                    
                    
                    #if cell is None:
                    print(f"creating new record for {member}")
                    # if not, create new record
                    length = len(worksheet.col_values(1))
                    worksheet.update(values=[[string_member_id, member.name, xp, level]], range_name=f'A{length+1}:D{length+1}')
                    """
                    cell = worksheet.cell(length+1,1)
                    worksheet.update_cell(length+1, 1, string_member_id)
                    worksheet.update_cell(length+1, 2, member.name)
                    worksheet.update_cell(length+1, 3, string_xp)
                    worksheet.update_cell(length+1, 4, string_level)
                    """

                    
                    else:
                        if cell:
                            continue
                            
                            print(f"updating record for {member}")
                            # if so, update that row...
                            # update exp, can only be in a positive direction
                            worksheet.update(values=[[xp, level]], range_name=f'C{cell.row}:D{cell.row}')

                            #worksheet.update_cell(cell.row, cell.col+2, xp)
                            #worksheet.update_cell(cell.row, cell.col+3, level)
                    

    
                    """
                    value = cell.value
                    row_number = cell.row
                    column_number = cell.col                
                    """
                      


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
