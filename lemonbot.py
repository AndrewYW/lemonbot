import discord, logging, json
import asyncio
import datetime
import pytz
import schedule
import toks
from tinydb import TinyDB, Query

db = TinyDB('data.json')
client = discord.Client()
Users = Query()

BIRTHDAY_ROLE = toks.BIRTHDAY_ROLE
BIRTHDAY_CHANNEL = toks.BIRTHDAY_CHANNEL
RESPONSE_CHANNEL = toks.RESPONSE_CHANNEL
LEMON_SERVER = toks.LEMON_SERVER
TESTING_CHANNEL = toks.TESTING_CHANNEL
TEST_ROLE = toks.TEST_ROLE
HOME_SERVER = toks.HOME_SERVER
OWNER_ID = toks.OWNER_ID
CLIENT_TOKEN = toks.CLIENT_TOKEN
KAIT_ID = toks.KAIT_ID
# Print the starting text
print('---------------')
print('lemonbot')
print('---------------')
print('Starting lemonbot...')

logging.basicConfig(level=logging.WARNING)

def getDate():
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
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
        if message.author.id == OWNER_ID: #dats me
            db.purge()
            await client.send_message(message.author, 'Birthday database purged!')
        else:
            await client.send_message(message.author, 'no')
            await client.send_file(message.channel, './res/img/unacceptable.png')
            msg = '{0.author.mention} has attempted to purge the db.'.format(message)
            await client.send_message(message.channel, msg)
            await client.send_message(message.channel, "Ahh! Atatatatat-No! That is why I'm royal, and *you* are servile!")
            await client.send_file(message.channel, './res/img/unacceptable.png')

    elif message.content.startswith("!status"):
        await client.send_message(message.channel, "Stop screaming! Why are you screaming?!")
    elif message.content.startswith('!purpose'):
        await client.send_file(message.channel, './res/img/purpose.png')
    elif message.content.startswith('!today'):
        date = getDate()
        msg = "Today's date is: {}/{}/{}".format(str(date['month']), str(date['day']), str(date['year']))
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!code'):
        await client.send_message(message.channel, 'https://github.com/AndrewYW/lemonbot')
    elif message.content.startswith('!bday'):
        if message.channel.id == BIRTHDAY_CHANNEL:
            if message.content == "!bday":
                await client.send_message(message.channel, "{0.author.mention}: Need to include month and day.".format(message))
            else:
                await client.delete_message(message)
                await bday_command(message)
    elif message.content.startswith('!list'):
        if message.author.id == OWNER_ID or message.author.id == KAIT_ID:
            doc = db.all()
            for item in doc:
                string = item['user'] + ', birthday: ' + str(item['month']) + ' ' + str(item['day'])
                await client.send_message(client.get_channel(RESPONSE_CHANNEL), string)

    elif message.content.startswith('!lemonbot'):
        await client.send_message(message.channel, """
            Lemonbot, the bot for lemons. 
            Commands list and formatting:
            [!status]: Checks status of bot.
            [!purpose]: Just try it.
            [!today]: Returns today's date in mm/dd/yyyy format.
            [!bday mm dd]: Adds your birthday to the database.
            [!code]: Links the Github repo of Lemonbot.
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
                'day': date,
                'birthday': False,
                'changed': False
            })
            await client.send_message(client.get_channel(RESPONSE_CHANNEL), 'Inserted into database: {0.author}'.format(message))
            await client.send_message(message.channel, '{0.author.mention}: Add success!'.format(message))
        else:
            if not Users.changed and Users.birthday:
                db.update({
                    'month': month,
                    'day': date,
                    'changed': True
                }, Users.id == auth.id)
                await client.send_message(message.channel, 'Updating birthday entry for: {0.author.mention}'.format(message))
                await client.send_message(client.get_channel(RESPONSE_CHANNEL), 'Updated entry for {0.author}'.format(message))
    else:
        await client.send_message(message.channel, "'They didn't understand my lemon styles. I like this way better.'")
        await client.send_message(message.channel, 'Proper format: "!bday mm dd"')

    
async def scrub_bdays(month, day):
    """
    Get all members of Lemon Fam
    Clear given role role from every member
    I really hope this works lmao
    """
    lemonServer = client.get_server(LEMON_SERVER)
    role = discord.utils.get(lemonServer.roles, id = BIRTHDAY_ROLE)
    birthdayLemons = db.search(Users.day != day)
    amount = "Removing: " + str(len(birthdayLemons)) + " members today"
    await client.send_message(client.get_channel(RESPONSE_CHANNEL), amount)
    if len(birthdayLemons) > 0:
        for doc in birthdayLemons:
            lemon = lemonServer.get_member(doc['id'])
            if lemon:
                if len(lemon.roles) > 0:
                    if role in lemon.roles:
                        await client.remove_roles(lemon, role)
                        await client.send_message(client.get_channel(RESPONSE_CHANNEL), "Removed role")
                

async def add_bdays(month, day):
    """
    Scan through database
    If doc birthday value matches today's date, add role to that member
    """
    lemonServer = client.get_server(LEMON_SERVER) #LEMON_SERVER
    birthdayLemons = db.search((Users.month == month) & (Users.day == day) & (Users.birthday==False))
    if len(birthdayLemons) > 0:
        amount = "Adding " + str(len(birthdayLemons)) + " members today"
        await client.send_message(client.get_channel(RESPONSE_CHANNEL), amount)
        for doc in birthdayLemons:
            lemon = lemonServer.get_member(doc['id'])
            db.update({'birthday': True}, Users.id == lemon.id)
            update = "Birthday today: " + str(lemon.name)
            await client.send_message(client.get_channel(RESPONSE_CHANNEL), update)
            role = discord.utils.get(lemonServer.roles, id=BIRTHDAY_ROLE)
            await client.add_roles(lemon, role) #BIRTHDAY_ROLE
            await client.send_message(client.get_channel(RESPONSE_CHANNEL), "Added role to a user")


async def daily_check():
    """
    Scan through database
    Return list of docs where birthday matches current date
    if birthday in members.roles
    For each document:
    """
    await client.wait_until_ready()
    while not client.is_closed:
        date = getDate()
        current = 'Current day: ' + str(date['month']) + "/" + str(date['day']) + "/" + str(date['year'])
        await client.send_message(client.get_channel(RESPONSE_CHANNEL), current ) #Private testing channel
        await scrub_bdays(date['month'], date['day'])
        await asyncio.sleep(10)
        await add_bdays(date['month'], date['day'])
        
        
        await asyncio.sleep(86400) #repeat daily -- 86400 seconds in a day



if __name__ == '__main__':
    client.loop.create_task(daily_check())
    client.run(CLIENT_TOKEN)
