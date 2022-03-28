from brownie import accounts, config, VoteStorage, network # type: ignore


def get_account():
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


owner = { 'from': get_account() }
