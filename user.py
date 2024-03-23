import argparse, requests
from helpers.splashscreen import splashscreen

# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--user_id", "-u", help="User ID", required=True)
parser.add_argument("--bot_token", "-b", help="Discord Bot Token")
parser.add_argument("--account_token", "-a", help="Discord Account Token")

args = parser.parse_args()

user_id = args.user_id

if args.bot_token is None and args.account_token is None:
    parser.error("A bot token or account token is required")
elif args.account_token is None:
    token = args.bot_token
    use_bot_token = True
else:
    token = args.account_token
    use_bot_token = False

premium_type = {
    0: "No Nitro",
    1: "Nitro Classic",
    2: "Nitro",
    3: "Nitro Basic"
}

print()
splashscreen()

# Get application info from Discord API
response = requests.get(f"https://discord.com/api/v10/users/{user_id}", headers={"Authorization": f"{"Bot " if use_bot_token else ""}{token}"})
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

    if not use_bot_token:
        # If using account token then access users profile
        response = requests.get(f"https://discord.com/api/v10/users/{user_id}/profile", headers={"Authorization": token})
        response = response.json()

        if "code" not in response:
            # Output user bio
            print("\n\x1b[1m\x1b[4mBio\x1b[0m")
            print(response["user"]["bio"])

            # Output all accounts connected to user
            print("\n\x1b[1m\x1b[4mConnected Accounts\x1b[0m")
            for account in response["connected_accounts"]:
                print(f"\x1b[1m{account["type"].upper()}{" "*(22-len(account["type"]))}\x1b[0m{account["id"]}")
        else:
            # If user profile cannot be accessed present an error message
            print("\n\x1b[1m\x1b[4mBio & Connected Accounts\x1b[0m\nCannot gather further data. You must share a server or be friends with the user.")
else:
    # If request failed present an error message
    print("\nUnknown user or Invalid token")

print()