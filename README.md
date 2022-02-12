Get Eth for Test network Rinkeby: https://faucets.chain.link/rinkeby

## Install Solidity Compiler
```commandline
pip install py-solc-x
```

## Install Web3
```commandline
pip install web3
```

## Create `.env` file and add the below
```commandline
export NETWORK_URL = http://test:test
export CHAIN_ID = 000
export MY_ADDRESS = 0x00000000000
export MY_PRIVATE_KEY = 0x0000000000000000

export FLASK_APP = Voting_System
export FLASK_ENV = development
```

## How to run...?
Build and Deploy
```commandline
python compile.py
python deploy.py
```

Run flask application
```commandline
python Voting_System.py
```
