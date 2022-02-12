import json
import os

from solcx import compile_standard, install_solc

SOL_VERSION = '0.8.11'
CONTRACT_NAME = 'VoteStorage'
FILE_NAME = f'{CONTRACT_NAME}.sol'
FILE_PATH = os.path.join('./', FILE_NAME)

with open(FILE_PATH, 'r') as f:
    sol_file = f.read()

# install_solc(SOL_VERSION)

compiled_sol = compile_standard(
    {
        'language': 'Solidity',
        'sources': {
            FILE_NAME: {
                'content': sol_file,
            },
        },
        'settings': {
            'outputSelection': {
                '*': {
                    '*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
                }
            }
        }
    },
    solc_version=SOL_VERSION
)

build_fle_path = f'./build/{FILE_NAME}/'
isExist = os.path.exists(build_fle_path)
if not isExist:
    os.makedirs(build_fle_path)

with open(f'{build_fle_path}{CONTRACT_NAME}.json', 'w+') as f:
    json.dump(compiled_sol, f, indent=4)
    print(f"Compiled code saved in {f.name}.")

with open(f'{build_fle_path}abi.json', 'w+') as f:
    json.dump(compiled_sol['contracts'][f'{CONTRACT_NAME}.sol'][CONTRACT_NAME]['abi'], f, indent=4)
    print(f"Compiled code saved in {f.name}.")
