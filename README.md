# DisTrace

Distrace is a collection of python scripts that are designed to assist in tracking, analysing, and disrupting malware campaigns that utilise Discord for command & control (C2).

> [!NOTE]
> This is intended for use by threat intelligence analysts, researchers, and security professionals.

Before starting use `pip install -r requirements.txt` to make sure that all requirements are installed.

There are 6 scripts included in DisTrace:

-   [bot.py](#botpy)
-   [webhook.py](#webhookpy)
-   [user.py](#userpy)
-   [application.py](#applicationpy)
-   [guild.py](#guildpy)
-   [file.py](#filepy)

Click any of the scripts to learn more about them.

> [!NOTE]
> If you use DisTrace in any research or anything published, credit or a shoutout would be appreciated!

DisTrace was inspired by [TeleTracker](https://github.com/tsale/TeleTracker).

## bot.py

bot.py is designed for working with Discord Bot tokens. It's capabilities depend on what privileged intents were enabled by the bot creator.

Run by `python bot.py -t DISCORD_BOT_TOKEN`

This script can retrieve:

-   Application
    -   Name
    -   ID
    -   Description
    -   Tags
-   Application Owner
    -   Username
    -   Display name
    -   ID
-   Privileged Intents
    -   Presence
    -   Guild members
    -   Message content
-   Bot
    -   Name
    -   ID
    -   Token
    -   Public
-   List of guilds the bot is in

Then after selecting a guild you can retrieve:

-   Guild
    -   Name
    -   ID
    -   Creation date and time
    -   Approx presence count
    -   Approx member count
    -   Icon
    -   Splash
    -   Banner
-   Owner _(If server members privileged intent is enabled)_
    -   Username
    -   Display name
    -   Nickname
    -   ID
-   Channels _(Can only get channels that are visible to the bot)_
    -   Type
        -   Text
        -   Voice
        -   Announcement
        -   Stage
        -   Forum
    -   ID
-   Members _(If server members privileged intent is enabled)_
    -   Presence _(If presences privileged intent is enabled)_
    -   Bot/Owner

A few options are then available:

-   Creating a temporary invite to a channel _(If bot has permission to create invites for the channel)_
-   Sending a text message in a selected channel

<br>

> [!WARNING]
> Creating an invite is logged to the servers audit log. Joining a server may also result in a welcome message.

## webhook.py

webhook.py is designed for analyzing Discord Webhooks.

Run by `python webhook.py -w DISCORD_WEBHOOK_URL`

Due to the limited nature of webhooks, no messages can be retrieved. However certain data can be retrieved:

-   Webhook
    -   Name
    -   ID
    -   Token
    -   Avatar
-   Guild
    -   ID
-   Channel
    -   ID
-   Creator
    -   Username
    -   Display name
    -   ID
    -   Avatar
    -   Nitro type

There are then a few options available:

-   Sending a text message to the channel
-   Sending a JSON message to the channel (allows for embeds and more advanced messages)
-   Deleting the webhook

## user.py

user.py is designed to assist with discovering information about a user from their user id.

Run by `python user.py -u USER_ID -a DISCORD_ACCOUNT_TOKEN -b DISCORD_BOT_TOKEN`

> [!NOTE]
> This script works with either an account token or a bot token. _(Both can be provided but the account token will be used)_ An account token can provide more detail if you have a common guild or are friends however.

> [!CAUTION] 
> **NEVER** share your account _(or bot token)_ with others as this will allow them access to your account _(or bot)_.

This script can retrieve:

-   Username
-   Display name
-   ID
-   Avatar
-   Nitro type

If you have provided a account token and either have a common guild or are friends with the user then the script can also retrieve:

-   Bio
-   Connected accounts
    -   Type
    -   ID

## application.py

application.py is designed to assist with discovering information about an application from its application id.

Run by `python application.py -a APPLICATION_ID`

This script can retrieve:

-   Application
    -   Name
    -   ID
    -   Description
    -   Tags
    -   Icon
-   Bot
    -   Public
-   Privileged Intents
    -   Presence
    -   Guild members
    -   Message content

## guild.py

guild.py is designed to help identify guilds from their guild IDs.

It works by taking a guild ID and checking:

1. Server Discovery
2. Discord Widget

This means that it will not work with all guilds.

Run by `python guild.py -g GUILD_ID`

If a server has discovery on then it can retrieve:

-   Name
-   ID
-   Invite
-   Locale
-   Creation date and time
-   Keywords
-   Approx presence count
-   Approx member count
-   Premium subs count
-   Icon
-   Splash
-   Banner

If the server has the discord widget enabled then it can retrieve:

-   Name
-   ID
-   Invite _(If invite channel is enabled)_
-   Widget HTML link
-   Approx presence count

## file.py

file.py is designed to assist with discovering information about a file that has been uploaded to Discord from its URL.

Run by `python file.py -f FILE_URL`

This script can retrieve:

-   URL
-   Type
-   Upload date and time

## Requirements

`requests` and `discord.py` are required. All other libraries are standard libraries that come with python.

## Disclaimer

This tool is solely designed to be used for threat intelligence purposes. Use these tools responsibly and ensure compliance with all laws and Discord's [terms of service](https://discord.com/terms).

I take no responsibility for the actions of users of this tool or what they do with it.

## Credits

This project was inspired by [TeleTracker](https://github.com/tsale/TeleTracker) by [tsale](https://github.com/tsale) which was showcased by [John Hammond](https://www.youtube.com/@_JohnHammond) in [Tracking Cybercriminals on Telegram](https://www.youtube.com/watch?v=_GD5mPN_URM).
