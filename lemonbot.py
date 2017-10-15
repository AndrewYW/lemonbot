import discord, logging, json
import asyncio
import datetime
import schedule
from tinydb import TinyDB, Query

db = TinyDB('data.json')
client = discord.Client()
Users = Query()

# Print the starting text
print('---------------')
print('lemonbot')
print('---------------')
print('Starting lemonbot...')

logging.basicConfig(level=logging.WARNING)

def getDate():
    now = datetime.datetime.now()
    date = {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
    }
    return date
@client.event
async def on_ready():
    print(client.user.name + ' Launched!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('!purge'):
        await client.delete_message(message)
        if message.author.id == '134134591597445130': #dats me
            db.purge()
            await client.send_message(message.author, 'Birthday database purged!')
        else:
            await client.send_message(message.author, 'no')
            await client.send_file(message.channel, './res/img/unacceptable.png')
            msg = '{0.author.mention} has attempted to purge the db.'.format(message)
            await client.send_message(message.channel, msg)
            await client.send_message(message.channel, "Ahh! Atatatatat-No! That is why I'm royal, and *you* are servile!")

    elif message.content.startswith("!status"):
        await client.send_message(message.channel, "Stop screaming! Why are you screaming?!")
    elif message.content.startswith('!purpose'):
        await client.send_file(message.channel, './res/img/purpose.png')
    elif message.content.startswith('!today'):
        date = getDate()
        msg = "Today's date is: {}/{}/{}".format(str(date['month']), str(date['day']), str(date['year']))
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!bday'):
        if message.channel.name == 'bottest': #this will need to change to proper channel id
            if message.content == "!bday help":
                await client.send_message(message.channel, "")
            else:
                await client.delete_message(message)
                await bday_command(message)
    elif message.content.startswith('!lemonbot'):
        await client.send_message(message.channel, """
        Lemonbot, the bot for lemons. 
        Commands list and formatting:
        [!status]: Checks status of bot.
        [!purpose]: Just try it.
        [!today]: Returns today's date in mm/dd/yyyy format.
        [!bday mm dd]: Adds your birthday to the database. Type [!bday help] for more information.
        """)
   
async def bday_command(message):
    auth = message.author
    temp = message.content.split(" ")
    if len(temp) == 3 and temp[1].isdigit() and temp[2].isdigit():
        month = int(temp[1])
        date = int(temp[2])
        if not db.contains(Users.id == auth.id):
            db.insert({
                'user': auth.name,
                'id': auth.id,
                'text': message.content,
                'month': month,
                'day': date
            })
            await client.send_message(message.channel, 'Inserted into database')
            await client.send_message(message.author, 'Add success!')
        else:
            db.update({
                'month': month,
                'day': date
            }, Users.id == auth.id)
            await client.send_message(message.channel, 'Updating Entry')
    else:
        await client.send_message(message.channel, "'They didn't understand my lemon styles. I like this way better.'")
        await client.send_message(message.channel, 'Proper format: "!bday mm dd"')

'''
async def search_command(message):
    auth = message.author
    """
    if db.contains((Users.user == auth) & (Users.text == '!bday gurdertermer')):
        await client.send_message(message.channel, str(type(Users.text)))
    """
    
    results = db.search(Users.user == auth)
    print(str(len(results)))
    for dic in results:
        if dic['text'] == '!bday gurdertermer':
            print("found")
            await client.send_message(message.channel, dic['text'])
'''
    
async def scrub_bdays():
    """
    Get all members of Lemon Fam
    Clear 'birthday' role from every member
    I really hope this works lmao
    """
    for server in client.servers:
        if server.name == 'Lemon Family': #needs to be ID as well
            members = server.members #iterable
            for member in members:
                for role in member.roles:
                    if role.name == 'birthday': #also ID fool why you doing this
                        member.roles.remove(role)
async def add_bdays():
    """
    Scan through database
    If doc birthday value matches today's date, add role to that member
    """

async def daily_check():
    """
    Scan through database
    Return list of docs where birthday matches current date
    if birthday in members.roles
    For each document:
    """
    await client.wait_until_ready()
    while not client.is_closed:
        await scrub_bdays()
        await add_bdays()
        await asyncio.sleep(86400) #repeat daily



if __name__ == '__main__':
    client.loop.create_task(daily_check())
    client.run("[token]")
