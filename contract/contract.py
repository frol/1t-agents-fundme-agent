import near
import json

@near.export
def fund():
    """
    Fund the target account with 2 NEAR tokens if the devpost profile was not previously funded.
    """
    if near.predecessor_account_id() != near.current_account_id():
        near.panic_str("Unauthorized")
        return

    args = json.loads(near.input())
    devpost_profile_username = args["devpost_profile_username"]
    target_account_id = args["account_id"]

    if near.storage_has_key(devpost_profile_username):
        near.panic_str("Already funded")
        return
    fund_amount = 2 * 10**24
    near.storage_write(devpost_profile_username, json.dumps({"funded_account_id": target_account_id, "funded_amount": fund_amount}))

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
    profile_details = near.storage_read(devpost_profile_username)
    if profile_details:
        near.value_return(profile_details)
    near.value_return("null")
