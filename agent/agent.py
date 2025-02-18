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

    faucet_account = env.set_near("1t-agents-fund.frol.near", env.env_vars["PRIVATE_ACCESS_KEY"])
    result = asyncio.run(faucet_account.call("1t-agents-fund.frol.near", "fund", args={"account_id": target_account_id}))

    env.add_reply(f"You were funded! {result}")

try:
    run(env)
except Exception as err:
    env.add_reply(f"Oops. Something went wrong: {err}")

env.request_user_input()
