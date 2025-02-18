import near
import json

@near.export
def fund():
    args = json.loads(near.input())
    target_account_id = args["account_id"]
    if target_account_id != 'frol.near':
        near.panic_str("Only frol.near can be funded")
        return
    promise = near.promise_batch_create(target_account_id)
    near.promise_batch_action_transfer(promise, 5 * 10**24)
    near.promise_return(promise)
