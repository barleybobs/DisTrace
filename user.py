import argparse, requests
from helpers.splashscreen import splashscreen

# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--user_id", "-u", help="User ID", required=True)
parser.add_argument("--token", "-t", help="Discord Bot Token", required=True)
args = parser.parse_args()

user_id = args.user_id
token = args.token

premium_type = {
    0: "No Nitro",
    1: "Nitro Classic",
    2: "Nitro",
    3: "Nitro Basic"
}

print()
splashscreen()

# Get application info from Discord API
response = requests.get(f"https://discord.com/api/v10/users/{user_id}", headers={"Authorization": f"Bot {token}"})
if response.status_code == 200:
    # If request succeeded
    response = response.json()

    # Output information about the user
    print("\n\x1b[1m\x1b[4mUser\x1b[0m")
    print(f"\x1b[1mUSERNAME              \x1b[0m{response["username"]}")
    print(f"\x1b[1mDISPLAY NAME          \x1b[0m{response["global_name"]}")
    print(f"\x1b[1mID                    \x1b[0m{response["id"]}")
    print(f"\x1b[1mAVATAR                \x1b[0mhttps://cdn.discordapp.com/avatars/{response["id"]}/{response["avatar"]}.jpg?size=2048")
    print(f"\x1b[1mNITRO TYPE            \x1b[0m{premium_type[response["premium_type"]]}")
else:
    # If request failed present an error message
    print("\nUnknown user or Invalid token")

print()