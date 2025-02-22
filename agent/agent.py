import asyncio
import json
import re
import requests
from nearai.agents.environment import Environment

PROMPT = {
    "role": "system",
    "content": "Analyze the user input and extract the devpost profile link. If it is provided, write the devpost link, otherwise write 'no devpost link'.",
}


def run(env: Environment):
    devpost_profile_link = env.completion([PROMPT] + env.list_messages())
    if "no devpost link" in devpost_profile_link.lower():
        env.add_reply(
            """Howdy! If you are a One Trillon Agents Hackathon participant, we have great news for you! You can receive 2 NEAR now.

            1. Update your DevPost profile with the near.ai skill tag and put the following message in your bio: "I would like to receive 2 NEAR to my account: <your NEAR account id>"
            2. Share your your DevPost profile link with me here"""
        )
        return

    env.add_agent_log(f"completion: {devpost_profile_link}")
    if not devpost_profile_link.startswith("https://devpost.com/"):
        env.add_reply("The provided link is not a DevPost profile link.")
        return

    devpost_profile_username = devpost_profile_link[len("https://devpost.com/") :]

    # TODO: Check if the user is a participant of the One Trillon Agents Hackathon
    if devpost_profile_username not in ["frolvlad", "frolvlad1"]:
        env.add_reply("You are not a participant of the One Trillon Agents Hackathon.")
        return

    faucet_account_id = env.env_vars.get(
        "FAUCET_ACCOUNT_ID", "1t-agents-fund.frol.near"
    )
    faucet_account = env.set_near(
        faucet_account_id, env.env_vars["FAUCET_PRIVATE_ACCESS_KEY"]
    )
    if asyncio.run(
        faucet_account.view(
            faucet_account_id,
            "get_funded_profile_details",
            args={"devpost_profile_username": devpost_profile_username},
        )
    ):
        env.add_reply(
            "You already received the funds. Thank you for participating in the One Trillon Agents Hackathon!"
        )
        return

    devpost_profile_html = requests.get(devpost_profile_link).text
    if "software portfolio | Devpost</title>" not in devpost_profile_html:
        env.add_reply(
            "The provided link is not a DevPost profile link. It looks like this https://devpost.com/frolvlad"
        )
        return

    if '<span class="cp-tag">near.ai</span>' not in devpost_profile_html:
        env.add_reply(
            "The provided DevPost profile does not have near.ai skill tag! Please add it to your profile. See https://devpost.com/frolvlad as example"
        )
        return

    DEVPOST_PROFILE_BIO_START_MARKER = '<p class="large" id="portfolio-user-bio">'
    devpost_profile_bio_start = devpost_profile_html.find(
        DEVPOST_PROFILE_BIO_START_MARKER
    )
    if devpost_profile_bio_start == -1:
        env.add_reply(
            "The provided DevPost profile does not have a bio. Please add it to your profile: 'I would like to receive 2 NEAR to my account: <your NEAR account id>'"
        )
        return
    devpost_profile_bio_end = devpost_profile_html.find(
        "</p>", devpost_profile_bio_start
    )
    devpost_profile_bio = devpost_profile_html[
        devpost_profile_bio_start
        + len(DEVPOST_PROFILE_BIO_START_MARKER) : devpost_profile_bio_end
    ].lower()
    target_account_id_re = re.search(
        r"receive 2 near to my account:\s*((([a-z\d]+[\-_])*[a-z\d]+\.)*([a-z\d]+[\-_])*[a-z\d]+)",
        devpost_profile_bio,
    )
    if not target_account_id_re:
        env.add_reply(
            "The provided DevPost profile bio does not contain your NEAR account id. Please, add it to your bio as: 'I would like to receive 2 NEAR to my account: <your NEAR account id>'"
        )
        return
    target_account_id = target_account_id_re.group(1)

    result = asyncio.run(
        faucet_account.call(
            faucet_account_id,
            "fund",
            args={
                "devpost_profile_username": devpost_profile_username,
                "account_id": target_account_id,
            },
        )
    )

    env.add_reply(f"You were funded! {json.dumps(result)}")


try:
    run(env)
except Exception as err:
    env.add_reply(f"Oops. Something went wrong: {err}")
