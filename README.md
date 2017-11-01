# lemonbot

A simple little Discord bot written to do some tasks for a Twitch community Discord server.

I was unable to attend HackRU this semester so in spite I spent part of the weekend writing this bot. More features will be added as I get the motivation to create them.

## Dependencies

- `discord.py`: Discord API wrapper

- `asyncio`: Asynchronous programming module for Python

- `Python 3.6.1`

- `TinyDB 3.6.0`

## Features

**Command list:**

```
!lemonbot: Provides commands list
!status: Posts a message if bot is live. (Upcoming: uptime of bot, user track count)
!purpose: Lists the uses of the bot
!today: Returns today's date in mm/dd/yyyy format.
!code: Link to github repository.
!bday: Adds birthday of user to tinyDB database. Format of entry: '!bday mm dd'. Leading zeros are ignored.
```

## Upcoming

- Assigning roles based on current date and birthday status of database entries.
- Role management?

### Should you use this bot?

Probably not, the features included are for relatively specific purposes, and there are other bots out there that have overlapping features, in a more robust and applicable form.