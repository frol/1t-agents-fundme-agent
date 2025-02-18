import near
import json

@near.export
def fund():
    if near.predecessor_account_id() != near.current_account_id():
        near.panic_str("Unauthorized")
        return

    args = json.loads(near.input())
    devpost_profile_username = args["devpost_profile_username"]
    target_account_id = args["account_id"]

    if near.storage_has_key(devpost_profile_username):
        near.panic_str("Already funded")
        return
    near.storage_write(devpost_profile_username, target_account_id)

    promise = near.promise_batch_create(target_account_id)
    near.promise_batch_action_transfer(promise, 5 * 10**24)
    near.promise_return(promise)
