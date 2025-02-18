import asyncio
import requests
from nearai.agents.environment import Environment


def run(env: Environment):
    prompt = {"role": "system", "content": "Analyze the user input and extract the devpost link and the NEAR wallet account id from it. If those are provided, write 'Developer details:' and the devpost link and the account id on the individual lines."}
    result = env.completion([prompt] + env.list_messages())
    if "Developer details:" not in result:
        env.add_reply("If you are a One Trillon Agents Hackathon participant, provide your DevPost profile link and the NEAR wallet account id to receive 5 NEAR tokens.")
        return

    # last_message = env.get_last_message()
    # env.add_reply(f"You said 2: {last_message['content']}")
    # last_message_text = last_message["content"]
    # if last_message_text != "Fund me":
    #     return
    #target_account_id = "frol.near"

    _, devpost_profile_link, target_account_id = result.split("\n")

    # TODO: verify the devpost link
    if not devpost_profile_link.startswith("https://devpost.com/"):
        env.add_reply("The provided link is not a DevPost profile link.")
        return

    devpost_profile_username = devpost_profile_link[len("https://devpost.com/"):]

    devpost_profile_html = requests.get(devpost_profile_link).text
    if "software portfolio | Devpost</title>" not in devpost_profile_html:
        env.add_reply("The provided link is not a DevPost profile link.")
        return

    if '<span class="cp-tag">near.ai</span>' not in devpost_profile_html:
        env.add_reply("The provided DevPost profile does not have near.ai skill tag! Please add it to your profile.")
        return

    faucet_account = env.set_near("1t-agents-fund.frol.near", env.env_vars["PRIVATE_ACCESS_KEY"])
    result = asyncio.run(faucet_account.call("1t-agents-fund.frol.near", "fund", args={"devpost_profile_username": devpost_profile_username, "account_id": target_account_id}))

    env.add_reply(f"You were funded! {result}")

try:
    run(env)
except Exception as err:
    env.add_reply(f"Oops. Something went wrong: {err}")

env.request_user_input()
