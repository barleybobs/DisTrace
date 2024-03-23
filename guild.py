import argparse, requests, re, json
from helpers.splashscreen import splashscreen

# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--guild_id', '-g', help="Discord Server Guild ID", required=True)
args = parser.parse_args()

guild_id = args.guild_id

print()
splashscreen()

# Get discovery page for guild id
response = requests.get("https://discord.com/servers/" + guild_id)

print("\n\x1b[1m\x1b[4mDiscovery Lookup\x1b[0m")
if response.status_code == 200:
    # If guild is on discovery page
    # Find JSON in HTML
    response = response.text
    response = json.loads(re.search(r"window\.__PRELOADED_STATE__ = (.+)<\/script>", response).group(1))

    # Output info from discovery page
    print(f"\x1b[1mNAME                  \x1b[0m{response["serverPage"]["guild"]["name"]}")
    print(f"\x1b[1mGUILD_ID              \x1b[0m{response["serverPage"]["guild"]["id"]}")
    print(f"\x1b[1mINVITE                \x1b[0mhttps://discord.gg/invite/{response["serverPage"]["guild"]["vanity_url_code"]}")
    print(f"\x1b[1mLOCALE                \x1b[0m{response["serverPage"]["guild"]["preferred_locale"]}")
    print(f"\x1b[1mCREATED               \x1b[0m{response["serverPage"]["guild"]["created_at"]} (ISO 8601)")
    print(f"\x1b[1mKEYWORDS              \x1b[0m{", ".join(response["serverPage"]["guild"]["keywords"])}")

    print(f"\x1b[1mAPPROX PRESENCE COUNT \x1b[0m{response["serverPage"]["guild"]["approximate_presence_count"]}")
    print(f"\x1b[1mAPPROX MEMBER COUNT   \x1b[0m{response["serverPage"]["guild"]["approximate_member_count"]}")
    print(f"\x1b[1mPREMIUM SUBS COUNT    \x1b[0m{response["serverPage"]["guild"]["premium_subscription_count"]}")

    print(f"\x1b[1mICON                  \x1b[0m{response["serverPage"]["guild"]["icon"]}")
    print(f"\x1b[1mSPLASH                \x1b[0m{response["serverPage"]["guild"]["splash"]}")
    print(f"\x1b[1mBANNER                \x1b[0mhttps://cdn.discordapp.com/banners/{response["serverPage"]["guild"]["id"]}/{response["serverPage"]["guild"]["banner"]}.jpg?size=2048")

else:
    # If discovery is not enabled for the server then present an error message
    print("Discovery not enabled")

# Get widget API
response = requests.get("https://discord.com/api/guilds/" + guild_id + "/widget.json")
response = response.json()

print("\n\x1b[1m\x1b[4mWidget JSON API\x1b[0m")
if "code" not in response:
    # If widget is enabled for the server
    # Output info from widget API
    print(f"\x1b[1mNAME                  \x1b[0m{response["name"]}")
    print(f"\x1b[1mGUILD_ID              \x1b[0m{response["id"]}")
    print(f"\x1b[1mINVITE                \x1b[0m{response["instant_invite"]}")
    print(f"\x1b[1mWIDGET HTML           \x1b[0mhttps://discord.com/widget?id={response["id"]}")

    print(f"\n\x1b[1mAPPROX PRESENCE COUNT \x1b[0m{response["presence_count"]}")

else:
    # If widget not enabled for the server then present an error message
    print("Widget not enabled")

print()