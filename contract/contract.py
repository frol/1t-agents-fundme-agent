import near
import json

@near.export
def fund():
    """
    Fund the target account with 2 NEAR tokens if the devpost profile was not previously funded.
    """
    if near.predecessor_account_id() != near.current_account_id():
        near.panic_utf8("Unauthorized")
        return

    args = json.loads(near.input())
    devpost_profile_username = args["devpost_profile_username"]
    target_account_id = args["account_id"]

    if near.storage_has_key(devpost_profile_username):
        near.panic_utf8("Already funded")
        return
    fund_amount = 2 * 10**24
    profile_details = json.dumps({"funded_account_id": target_account_id})
    near.storage_write(devpost_profile_username, profile_details)

    promise = near.promise_batch_create(target_account_id)
    near.promise_batch_action_transfer(promise, fund_amount)
    near.promise_return(promise)

@near.export
def get_funded_profile_details():
    """
    Read the funded profile details JSON from the contract state and return it.
    """
    args = json.loads(near.input())
    devpost_profile_username = args["devpost_profile_username"]
    profile_details_exists, profile_details = near.storage_read(devpost_profile_username)
    if profile_details_exists:
        near.value_return(profile_details)
    else:
        near.value_return("null")

@near.export
def reset():
    """
    Reset the funded profile details for the given devpost profile usernames.
    """
    if near.predecessor_account_id() != near.current_account_id():
        near.panic_utf8("Unauthorized")
        return

    args = json.loads(near.input())
    for devpost_profile_username in args["devpost_profile_usernames"]:
        near.storage_remove(devpost_profile_username)
