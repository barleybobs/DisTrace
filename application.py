import argparse, requests
from helpers.splashscreen import splashscreen

# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--application_id", "-a", help="Application ID", required=True)
args = parser.parse_args()

application_id = args.application_id

print()
splashscreen()

# Get application info from Discord API
response = requests.get(f"https://discord.com/api/v10/applications/{application_id}/rpc")
if response.status_code == 200:
    # If request succeeded
    response = response.json()

    # Output information about the application
    print("\n\x1b[1m\x1b[4mApplication\x1b[0m")
    print(f"\x1b[1mNAME                  \x1b[0m{response["name"]}")
    print(f"\x1b[1mID                    \x1b[0m{response["id"]}")
    print(f"\x1b[1mDESCRIPTION           \x1b[0m{response["description"]}")
    print(f"\x1b[1mTAGS                  \x1b[0m{", ".join(response["tags"])}")
    print(f"\x1b[1mICON                  \x1b[0m{response["icon"]}")

    # Output information about the associated bot
    print("\n\x1b[1m\x1b[4mBot\x1b[0m")
    print(f"\x1b[1mPUBLIC                \x1b[0m{response["bot_public"]}")

    # Output information about the privileged intents and their scope
    # https://discord.com/developers/docs/resources/application#application-object-application-flags
    print("\n\x1b[1m\x1b[4mPrivileged Intents\x1b[0m")
    print(f"\x1b[1mPRESENCE              \x1b[0m{"Limited" if response["flags"] & 1<<13 else ("Unlimited" if response["flags"] & 1<<12 else "None")}")
    print(f"\x1b[1mGUILD MEMBERS         \x1b[0m{"Limited" if response["flags"] & 1<<15 else ("Unlimited" if response["flags"] & 1<<14 else "None")}")
    print(f"\x1b[1mMESSAGE CONTENT       \x1b[0m{"Limited" if response["flags"] & 1<<19 else ("Unlimited" if response["flags"] & 1<<18 else "None")}")
else:
    # If request failed present an error message
    print("\nUnknown application")

print()