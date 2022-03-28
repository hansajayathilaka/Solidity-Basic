from brownie import DynamicVoteStorage, config, network # type: ignore
from .utils import owner


def deploy_vote_storage():
    voteStorage = DynamicVoteStorage.deploy(
        owner,
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f'Contract deployed to {voteStorage.address}')


def main():
    deploy_vote_storage()
