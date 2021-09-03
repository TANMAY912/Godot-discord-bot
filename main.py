import discord
import asyncio
from datetime import datetime
import pytz
import re
import os

intents = discord.Intents().all()
intents.members = True

TOKEN = os.environ['TOKEN_SECRET']

client = discord.Client(intents=intents)

coroutineDict = dict()
statusDict = dict()

async def bootup():
    await client.wait_until_ready()
    print("Started")
    global monitorFlag
    monitorFlag = True
    allChannels = client.get_all_channels()
    for channel in allChannels:
        if str(channel.type) == 'text':
            try:
                # await channel.send('Monitoring every member')
                # await channel.send('<a:tooFunnySphere:872414709167583272>')
                client.loop.create_task(statusLooper(channel))
            except:
                pass
    print("Startup processes completed")

@client.event
async def on_ready():
    print('Bot Online')

async def messageLooper(message):
    while True:
        msg = '<a:tooFunnySphere:872414709167583272>'
        await message.channel.send(msg)
        await asyncio.sleep(32400)

async def statusLooper(channel):
    while True:
        for member in channel.guild.members:
            if str(member.status) == 'online':
                statusDict[member] = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%B %d, %Y %H:%M:%S %Z')
        await asyncio.sleep(60)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if '<a:tooFunnySphere:872414709167583272>' in message.content:
        await message.channel.send('<a:tooFunnySphere:872414709167583272>')

    if message.content.startswith('!spam') or message.content.startswith('! spam'):
        for i in range(5):
            msg = '<a:tooFunnySphere:872414709167583272>'
            await message.channel.send(msg)

    if message.content.startswith('!commands') or message.content.startswith('! commands'):
        # info_string = ('List of commands:\n'
        #                 '!spam: spams the best emote ever\n'
        #                 '!loop: sends a fixed message periodically in the channel\n'
        #                 '!stop: stops the loop running in the channel\n'
        #                 '!ping: pings the mentioned user 7 times atm, (8 if the original command is included)')
        # # await message.channel.send('```' + info_string + '```')
        embed=discord.Embed(title="**Godot Bot Info**", url="https://www.youtube.com/watch?v=xvFZjo5PgG0", description="A discord bot made for fun\nCommands start with `!`", color=0x0088ff)
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/pw/AM-JKLXxpXJbLWT7lnK59M4-lPVZvlk00CIxreXN6epYWXS1N852nWJr8n1JUTLAV8Nwu2v7O1X1AnW4hEZpzfvIpoXY0NgeAuAWSiSqOxBCn_CtvwZZQmAlwsHyNhhzf_DAts0KSWptcvxroHbrsKllpkqV=s795-no")
        embed.add_field(name="\u200b", value="**List of commands**", inline=False)
        embed.add_field(name="`!spam or ! spam`", value="> Spams the best emote ever", inline=False)
        embed.add_field(name="`!loop or ! loop`", value="> Sends a fixed message periodically in the channel", inline=False)
        embed.add_field(name="`!stop or ! stop`", value="> Stops the loop running in the channel", inline=False)
        embed.add_field(name="`!ping <user> <number(optional)> or ! ping <user> <number(optional)>`", value="> Tags the mentioned user specified number of times, 7 times if no amount is specified", inline=False)
        embed.add_field(name="`!monitor or ! monitor`", value="> The bots starts to monitor status of every member in the server", inline=False)
        embed.add_field(name="`!getstatus <user> or ! getstatus <user>`", value="> Returns the time when the user was last online", inline=False)
        await message.channel.send(embed = embed)

    if message.content.startswith('!botinfo') or message.content.startswith('! botinfo'):
        await message.channel.send('No info for you')
        await message.channel.send('<a:PaimonTantrum:874692011490414642>')

    if message.content.startswith('!loop') or message.content.startswith('! loop'):
        if message.channel in coroutineDict.keys():
            await message.channel.send('A loop is already running on this channel')
        else:
            task = asyncio.ensure_future(messageLooper(message))
            coroutineDict[message.channel] = task

    if message.content.startswith('!stop') or message.content.startswith('! stop'):
        if message.channel in coroutineDict.keys():
            coroutineDict[message.channel].cancel()
            del coroutineDict[message.channel]
            await message.channel.send('The loop is stopped')
        else:
            await message.channel.send('There is no loop running on this channel')

    if message.content.startswith('!ping') or message.content.startswith('! ping'):
        # print("ok")
        spl = message.content.rsplit()
        # print(spl)
        # print(len(spl))
        if spl[0] == '!ping':
            if len(spl) == 2:
                # print(spl[1])
                if spl[1][0:2] != '<@' or spl[1][-1] != '>':
                    await message.channel.send('{0.author.mention}'.format(message) + ' Type a valid username')
                    await message.channel.send('<a:PaimonTantrum:874692011490414642>')
                else:
                    for i in range(7):
                        await message.channel.send(spl[1])

            elif len(spl) == 3:
                try:
                    count = int(spl[2])
                    if count >= 10:
                        await message.channel.send('{0.author.mention}'.format(message) + ' Calm down, that\'s too many pings')
                    else:
                        if spl[1][0:2] != '<@' or spl[1][-1] != '>':
                            await message.channel.send('{0.author.mention}'.format(message) + ' Type a valid username')
                            await message.channel.send('<a:PaimonTantrum:874692011490414642>')
                        else:
                            for i in range(count):
                                await message.channel.send(spl[1])
                except Exception as e:
                    await message.channel.send('{0.author.mention}'.format(message) + ' Enter a valid integer')
                    await message.channel.send('<a:PaimonTantrum:874692011490414642>')

            else:
                await message.channel.send('{0.author.mention}'.format(message) + ' follow the format')
                await message.channel.send('<a:PaimonTantrum:874692011490414642>')
        elif spl[0] == '!':
                if len(spl) == 3:
                    # print(spl[1])
                    if spl[2][0:2] != '<@' or spl[2][-1] != '>':
                        await message.channel.send('{0.author.mention}'.format(message) + ' Type a valid username')
                        await message.channel.send('<a:PaimonTantrum:874692011490414642>')
                    else:
                        for i in range(7):
                            await message.channel.send(spl[2])

                elif len(spl) == 4:
                    try:
                        count = int(spl[3])
                        if count >= 10:
                            await message.channel.send('{0.author.mention}'.format(message) + ' Calm down, that\'s too many pings')
                        else:
                            if spl[2][0:2] != '<@' or spl[2][-1] != '>':
                                await message.channel.send('{0.author.mention}'.format(message) + ' Type a valid username')
                                await message.channel.send('<a:PaimonTantrum:874692011490414642>')
                            else:
                                for i in range(count):
                                    await message.channel.send(spl[2])
                    except Exception as e:
                        await message.channel.send('{0.author.mention}'.format(message) + ' Enter a valid integer')
                        await message.channel.send('<a:PaimonTantrum:874692011490414642>')

                else:
                    await message.channel.send('{0.author.mention}'.format(message) + ' follow the format')
                    await message.channel.send('<a:PaimonTantrum:874692011490414642>')


    if message.content.startswith('!monitor') or message.content.startswith('! monitor'):
        spl = message.content.rsplit()
        if spl[0] == '!monitor':
            if len(spl) != 1:
                await message.channel.send('Extra arguments provided <a:PaimonTantrum:874692011490414642>')
            elif monitorFlag:
                await message.channel.send('The server is already being monitored')
                # await message.channel.send('<a:tooFunnySphere:872414709167583272>')
            else:
                await message.channel.send('Monitoring every member')
                await message.channel.send('<a:tooFunnySphere:872414709167583272>')
        elif spl[0] == '!':
            if len(spl) != 2:
                await message.channel.send('Extra arguments provided <a:PaimonTantrum:874692011490414642>')
            elif monitorFlag:
                await message.channel.send('The server is already being monitored')
                # await message.channel.send('<a:tooFunnySphere:872414709167583272>')
            else:
                await message.channel.send('Monitoring every member')
                await message.channel.send('<a:tooFunnySphere:872414709167583272>')
        # for guild in client.guilds:
        # for member in message.guild.members:
            # await message.channel.send(str(member) + ' -> ' + str(member.status))

    # if message.content.startswith('!type'):
    #     print(type(message.author))


    if message.content.startswith('!getstatus') or message.content.startswith('! getstatus'):

        spl = message.content.rsplit()
        # print(len(spl))
        if spl[0] == '!getstatus':
            if len(spl) == 2:
                # await message.channel.send(spl[1] == message.author)
                # await message.channel.send(message.author)
                # await message.channel.send(spl[1])
                # print(spl[1])
                # await message.channel.send(client.get_user(int(re.sub("[^0-9]", "", spl[1]))) == message.author)
                # print(int(re.sub("[^0-9]", "", spl[1])))
                if client.get_user(int(re.sub("[^0-9]", "", spl[1]))) in statusDict.keys():
                    await message.channel.send('Last online: ' + str(statusDict[client.get_user(int(re.sub("[^0-9]", "", spl[1])))]))
                else:
                    await message.channel.send("The user has been inactive since the bot started monitoring")

                # for member in message.guild.members:

                    # await message.channel.send(str(member) + ' -> ' + str(member.status))
                #     if member = spl[1]

            else:
                await message.channel.send('{0.author.mention}'.format(message) + ' follow the format')
                await message.channel.send('<a:PaimonTantrum:874692011490414642>')
        elif spl[0] == '!':
            if len(spl) == 3:
                # await message.channel.send(spl[1] == message.author)
                # await message.channel.send(message.author)
                # await message.channel.send(spl[1])
                # print(spl[1])
                # await message.channel.send(client.get_user(int(re.sub("[^0-9]", "", spl[1]))) == message.author)
                # print(int(re.sub("[^0-9]", "", spl[1])))
                if client.get_user(int(re.sub("[^0-9]", "", spl[2]))) in statusDict.keys():
                    await message.channel.send('Last online: ' + str(statusDict[client.get_user(int(re.sub("[^0-9]", "", spl[2])))]))
                else:
                    await message.channel.send("The user has been inactive since the bot started monitoring")

                # for member in message.guild.members:

                    # await message.channel.send(str(member) + ' -> ' + str(member.status))
                #     if member = spl[1]

            else:
                await message.channel.send('{0.author.mention}'.format(message) + ' follow the format')
                await message.channel.send('<a:PaimonTantrum:874692011490414642>')

client.loop.create_task(bootup())
client.run(TOKEN)
