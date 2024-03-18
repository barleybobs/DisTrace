import argparse, requests, json
from helpers.splashscreen import splashscreen

# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--webhook', '-w', help="Discord Webhook URL", required=True)
args = parser.parse_args()

webhook_url = args.webhook

premium_type = {
    0: "No Nitro",
    1: "Nitro Classic",
    2: "Nitro",
    3: "Nitro Basic"
}

print()
splashscreen()

# Get info about the webhook from the webhook URL
response = requests.get(webhook_url)
if response.status_code == 200:
    # If request succeeded
    # Process JSON response
    response = response.json()

    # Output info about the webhook
    print("\n\x1b[1m\x1b[4mWebhook\x1b[0m")
    print(f"\x1b[1mNAME                  \x1b[0m{response["name"]}")
    print(f"\x1b[1mID                    \x1b[0m{response["id"]}")
    print(f"\x1b[1mTOKEN                 \x1b[0m{response["token"]}")
    print(f"\x1b[1mAVATAR                \x1b[0m{"None" if response["avatar"] == None else f"https://cdn.discordapp.com/avatars/{response["id"]}/{response["avatar"]}.jpg?size=2048"}")

    # Output info about the guild that the webhook belongs to
    print("\n\x1b[1m\x1b[4mGuild\x1b[0m")
    print(f"\x1b[1mGUILD ID              \x1b[0m{response["guild_id"]}")
    print(f"\x1b[1mCHANNEL ID            \x1b[0m{response["channel_id"]}")

    # Output info about the webhook owner/creator
    print("\n\x1b[1m\x1b[4mCreator\x1b[0m")
    print(f"\x1b[1mUSERNAME              \x1b[0m{response["user"]["username"]}")
    print(f"\x1b[1mDISPLAY NAME          \x1b[0m{response["user"]["global_name"]}")
    print(f"\x1b[1mID                    \x1b[0m{response["user"]["id"]}")
    print(f"\x1b[1mAVATAR                \x1b[0mhttps://cdn.discordapp.com/avatars/{response["user"]["id"]}/{response["user"]["avatar"]}.jpg?size=2048")
    print(f"\x1b[1mNITRO TYPE            \x1b[0m{premium_type[response["user"]["premium_type"]]}")

    # Present the user with options
    print("\n\x1b[1m\x1b[4mOptions:\x1b[0m")
    print("1. Send a text message to the discord channel")
    print("2. Send JSON message to the discord channel")
    print("3. Delete Webhook")
    print("4. EXIT")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        # Send a text message to the channel
        message = input("\nEnter your message: ")

        response = requests.post(webhook_url, data=json.dumps({"content": message}), headers={'Content-Type': 'application/json'})

        if response.status_code == 200 or response.status_code == 204:
            print("\nMessage sent successfully")
        elif response.status_code == 400:
            print("\nInvalid JSON")
        else:
            print("\nFailed to send message")

    elif choice == "2":
        # Send a JSON message (allows for stuff like embeds) to the channel
        message_json = input("\nEnter JSON: ")

        response = requests.post(webhook_url, data=message_json, headers={'Content-Type': 'application/json'})

        if response.status_code == 200 or response.status_code == 204:
            print("\nMessage sent successfully")
        elif response.status_code == 400:
            print("\nInvalid JSON")
        else:
            print("\nFailed to send message")

    elif choice == "3":
        # Delete the webhook
        response = requests.delete(webhook_url)

        if response.status_code == 200 or response.status_code == 204:
            print("\nWebhook deleted successfully")
        else:
            print("\nFailed to delete webhook")
else:
    # If request failed present an error message
    print("\nCannot access webhook")

print()