import argparse, discord
from helpers.splashscreen import splashscreen

# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--token", "-t", help="Discord Bot Token", required=True)
args = parser.parse_args()

token = args.token

print()
splashscreen()

# Check which privileged intents are enabled
privileged_intents_check_client = discord.Client(intents=discord.Intents.default())

@privileged_intents_check_client.event
async def on_ready():
    application_info = await privileged_intents_check_client.application_info()

    global privileged_intents_presences
    global privileged_intents_members
    global privileged_intents_messages

    privileged_intents_presences = application_info.flags.gateway_presence or application_info.flags.gateway_presence_limited
    privileged_intents_members = application_info.flags.gateway_guild_members or application_info.flags.gateway_guild_members_limited
    privileged_intents_messages = application_info.flags.gateway_message_content or application_info.flags.gateway_message_content_limited

    await privileged_intents_check_client.http.close()
    await privileged_intents_check_client.close()

try:
    privileged_intents_check_client.run(token, log_handler=None)
except discord.errors.LoginFailure as e:
    # If failed to login
    print("\nFailed to login. Double check your bot token.")

# Create the main client with the enabled privileged intents
intents = discord.Intents(guilds=True, presences=privileged_intents_presences, members=privileged_intents_members, messages=privileged_intents_messages)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    application_info = await client.application_info()

    print("\n\x1b[1m\x1b[4mApplication\x1b[0m")
    print(f"\x1b[1mNAME                  \x1b[0m{application_info.name}")
    print(f"\x1b[1mID                    \x1b[0m{client.user.id}")
    print(f"\x1b[1mDESCRIPTION           \x1b[0m{application_info.description}")
    print(f"\x1b[1mTAGS                  \x1b[0m{", ".join(application_info.tags)}")
    print(f"\x1b[1mICON                  \x1b[0m{application_info.icon}")

    print("\n\x1b[1m\x1b[4mApplication Owner\x1b[0m")
    print(f"\x1b[1mUSERNAME              \x1b[0m{application_info.owner.name}")
    print(f"\x1b[1mDISPLAY NAME          \x1b[0m{application_info.owner.global_name}")
    print(f"\x1b[1mID                    \x1b[0m{application_info.owner.id}")

    print("\n\x1b[1m\x1b[4mPrivileged Intents\x1b[0m")
    print(f"\x1b[1mPRESENCE              \x1b[0m{"Limited" if application_info.flags.gateway_presence_limited else ("Unlimited" if application_info.flags.gateway_presence else "None")}")
    print(f"\x1b[1mGUILD MEMBERS         \x1b[0m{"Limited" if application_info.flags.gateway_guild_members_limited else ("Unlimited" if application_info.flags.gateway_guild_members else "None")}")
    print(f"\x1b[1mMESSAGE CONTENT       \x1b[0m{"Limited" if application_info.flags.gateway_message_content_limited else ("Unlimited" if application_info.flags.gateway_message_content else "None")}")

    # Output information about the bot
    print("\n\x1b[1m\x1b[4mBot\x1b[0m")
    print(f"\x1b[1mNAME                  \x1b[0m{client.user.name}")
    print(f"\x1b[1mID                    \x1b[0m{client.user.id}")
    print(f"\x1b[1mTOKEN                 \x1b[0m{token}")
    print(f"\x1b[1mPUBLIC                \x1b[0m{application_info.bot_public}")

    # Output a list of guilds the bot is in
    print("\n\x1b[1m\x1b[4mGuilds bot is in\x1b[0m")
    for guild in client.guilds:
        print(f"\x1b[1m{guild.id}   \x1b[0m{guild.name}")

    # Ask the user to pick a guild to get more details and carry out actions on
    chosen_guild = client.get_guild(int(input("\nEnter Guild ID: ")))

    if chosen_guild == None:
        # If the bot isn't in the given guild then present an error message  
        print("\nBot is not in that guild")

        await client.http.close()
        await client.close()
    else:
        # Output information about the guild
        print("\n\x1b[1m\x1b[4mGuild\x1b[0m")
        print(f"\x1b[1mNAME                  \x1b[0m{chosen_guild.name}")
        print(f"\x1b[1mID                    \x1b[0m{chosen_guild.id}")
        print(f"\x1b[1mCREATED               \x1b[0m{chosen_guild.created_at}")

        # To get approx presence and member count you have to fetch the guild
        fetched_chosen_guild = await client.fetch_guild(chosen_guild.id)
        print(
            f"\x1b[1mAPPROX PRESENCE COUNT \x1b[0m{fetched_chosen_guild.approximate_presence_count}"
        )
        print(
            f"\x1b[1mAPPROX MEMBER COUNT   \x1b[0m{fetched_chosen_guild.approximate_member_count}"
        )

        # These will be None if they are not set
        print(f"\x1b[1mICON                  \x1b[0m{chosen_guild.icon}")
        print(f"\x1b[1mSPLASH                \x1b[0m{chosen_guild.banner}")
        print(f"\x1b[1mBANNER                \x1b[0m{chosen_guild.splash}")

        print("\n\x1b[1m\x1b[4mOwner\x1b[0m")
        if client.intents.members:
            # If members intent is enabled then output owner details
            print(f"\x1b[1mUSERNAME              \x1b[0m{chosen_guild.owner.name}")
            print(f"\x1b[1mDISPLAY NAME          \x1b[0m{chosen_guild.owner.global_name}")
            print(f"\x1b[1mNICKNAME              \x1b[0m{chosen_guild.owner.nick}")
            print(f"\x1b[1mID                    \x1b[0m{chosen_guild.owner.id}")
        else:
            print("Members intent disabled")

        print("\n\x1b[1m\x1b[4mChannels\x1b[0m")
        # Text channels
        for (i, channel) in enumerate(filter(lambda channel: not channel.is_news(), chosen_guild.text_channels)):
            print(f"\x1b[1m{"TEXT" if i == 0 else " "*4}                  \x1b[0m{channel.name}{" "*(22-len(channel.name))}\x1b[90m({channel.id})\x1b[0m")
        # Voice channels
        for (i, channel) in enumerate(chosen_guild.voice_channels):
            print(f"\x1b[1m{"VOICE" if i == 0 else " "*5}                 \x1b[0m{channel.name}{" "*(22-len(channel.name))}\x1b[90m({channel.id})\x1b[0m")
        # Announcement channels
        for (i, channel) in enumerate(filter(lambda channel: channel.is_news(), chosen_guild.text_channels)):
            print(f"\x1b[1m{"ANNOUNCEMENT" if i == 0 else " "*12}          \x1b[0m{channel.name}{" "*(22-len(channel.name))}\x1b[90m({channel.id})\x1b[0m")
        # Stage channels
        for (i, channel) in enumerate(chosen_guild.stage_channels):
            print(f"\x1b[1m{"STAGE" if i == 0 else " "*5}                 \x1b[0m{channel.name}{" "*(22-len(channel.name))}\x1b[90m({channel.id})\x1b[0m")
        # Forums
        for (i, channel) in enumerate(chosen_guild.forums):
            print(f"\x1b[1m{"FORUM" if i == 0 else " "*5}                 \x1b[0m{channel.name}{" "*(22-len(channel.name))}\x1b[90m({channel.id})\x1b[0m")
        print("\x1b[90mN.B. This will only display channels visible to the bot. This may not be a complete list.\x1b[0m")

        print("\n\x1b[1m\x1b[4mMembers\x1b[0m")
        if not client.intents.members:
            # If presences intent is disabled then present an error message
            print("Members intent disabled")
        elif client.intents.presences:
            # Sort members by status
            members = {"ONLINE": [], "IDLE": [], "DO NOT DISTURB": [], "OFFLINE": []}
            for member in chosen_guild.members:
                if str(member.status) == "online":
                    members["ONLINE"].append(member)
                elif str(member.status) == "idle":
                    members["IDLE"].append(member)
                elif str(member.status) == "dnd" or str(member.status) == "do_not_disturb":
                    members["DO NOT DISTURB"].append(member)
                elif str(member.status) == "offline" or str(member.status) == "invisible":
                    members["OFFLINE"].append(member)
            # Output members list with members status
            for status in members:
                for (i, member) in enumerate(members[status]):
                    print(f"\x1b[1m{status + " "*(22-len(status)) if i == 0 else " "*22}\x1b[0m{member.name}{" "*(22-len(member.name))}\x1b[90m({member.id}) ", end="")
                    if member.bot == True:
                        print("(Bot)\x1b[0m")
                    elif member.id == chosen_guild.owner.id:
                        print("(Owner)\x1b[0m")
                    else:
                        print("\x1b[0m")
        else:
            # Output members list without members status due to presences intent being disabled
            for (i, member) in enumerate(chosen_guild.members):
                print(f"{"\x1b[1mUNKNOWN               " if i == 0 else " "*22}\x1b[0m{member.name}{" "*(22-len(member.name))}\x1b[90m({member.id}) ", end="")
                if member.bot == True:
                    print("(Bot)\x1b[0m")
                elif member.id == chosen_guild.owner.id:
                    print("(Owner)\x1b[0m")
                else:
                    print("\x1b[0m")
            print("\x1b[90mN.B. Unknown displayed as presences intent is disabled.\x1b[0m")

        # Present the user with options
        print("\n\x1b[1m\x1b[4mOptions:\x1b[0m")
        print("1. Create a temporary invite to a channel")
        print("2. Send a message in a text channel")
        print("3. EXIT")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            # Create a temporary invite to a chosen channel
            chosen_channel = chosen_guild.get_channel(int(input("\nEnter Channel ID: ")))
            if chosen_channel == None:
                print("\nChannel is not in the guild")

                await client.http.close()
                await client.close()
            else:
                print("\n\x1b[1m\x1b[4mInvite URL\x1b[0m")
                if chosen_channel.permissions_for(chosen_guild.me).create_instant_invite:
                    print(await chosen_channel.create_invite(max_age=120, max_uses=1, unique=True))
                else:
                    print("Bot does not have permission to create invites in the channel.")

        elif choice == "2":
            # Send a message to a chosen channel
            chosen_channel = chosen_guild.get_channel(int(input("\nEnter Channel ID: ")))
            if chosen_channel == None:
                print("\nChannel is not in the guild")

                await client.http.close()
                await client.close()
            else:
                sent_message = await chosen_channel.send(input("\nEnter Message: "))

                if sent_message == None:
                    print("\nMessage failed to send")
                else:
                    print("\nMessage sent successfully")


        # Exit discord bot client
        await client.http.close()
        await client.close() 

# Try starting client
try:
    client.run(token, log_handler=None)
except discord.errors.LoginFailure as e:
    # If failed to login
    print("\nFailed to login. Double check your bot token.")

print()