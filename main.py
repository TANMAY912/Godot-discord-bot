# Work with Python 3.6
import discord
import asyncio
import time

TOKEN = 'ODc0NTYzMDk4MTY4NjY4MjEx.YRIyWw.muBUANiaUPIhxcWQ0wAowRfWdfc'

client = discord.Client()

stop = False

async def PingHandler(message):
    print("ok")
    spl = message.content.rsplit()
    print(len(spl))
    if len(spl) != 2:
        await message.channel.send('{0.author.mention}'.format(message))
        return
    else:
        # msg = spl[1]
        await message.channel.send(spl[1])



async def looper(message):
    while not stop:
        msg = '<a:tooFunnySphere:872414709167583272>'
        await message.channel.send(msg)
        await asyncio.sleep(32400)

    print('exit')

@client.event
async def on_message(message):
    # print(message.content)
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if '<a:tooFunnySphere:872414709167583272>' in message.content:
        await message.channel.send('<a:tooFunnySphere:872414709167583272>')

    if message.content.startswith('!spam'):
        for i in range(5):
            msg = '<a:tooFunnySphere:872414709167583272>'
            await message.channel.send(msg)

    if message.content.startswith('!commands'):
        info_string = 'List of commands:\n!spam: spams the best emote ever\n!loop: sends a fixed message periodically, cannot be stopped\n!ping: pings the mentioned user 7 times atm, (8 if the original command is included)'
        await message.channel.send('```' + info_string + '```')

    if message.content.startswith('!botinfo'):
        await message.channel.send('No info for you')
        await message.channel.send('<a:PaimonTantrum:874692011490414642>')

    if message.content.startswith('!loop'):
        # msg = '<a:tooFunnySphere:872414709167583272>'
        task = asyncio.ensure_future(looper(message))
        # print(type(task))
        # await message.channel.send(msg)

    if message.content.startswith('!ping'):
        print("ok")
        spl = message.content.rsplit()
        print(len(spl))
        if len(spl) == 2:
            print(spl[1])
            if spl[1][0:2] != '<@' or spl[1][-1] != '>':
                await message.channel.send('{0.author.mention}'.format(message) + ' Type a valid username')
                await message.channel.send('<a:PaimonTantrum:874692011490414642>')
                    # await message.channel.send('{0.author.mention}'.format(message) + ' ?')
            else:
                for i in range(7):
                    await message.channel.send(spl[1])

        elif len(spl) == 3:
            try:
                count = int(spl[2])
                if count >= 10:
                    await message.channel.send('{0.author.mention}'.format(message) + ' Calm down, that\'s too many pings')
                else:
                    for i in range(count):
                        await message.channel.send(spl[1])
            except Exception as e:
                await message.channel.send('{0.author.mention}'.format(message) + ' Enter a valid integer')
                await message.channel.send('<a:PaimonTantrum:874692011490414642>')

        else:
            await message.channel.send('{0.author.mention}'.format(message) + ' follow the format')
            await message.channel.send('<a:PaimonTantrum:874692011490414642>')


    if message.content.startswith('!stop'):
        stop = True
        task.cancel
        msg = 'stp'
        await message.channel.send(msg)





@client.event
async def on_ready():
    print('Bot online')
    # print(client.user.name)
    # print(client.user.id)
    # print('------')

client.run(TOKEN)
