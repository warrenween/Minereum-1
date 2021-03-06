# Minereum
A short script to mine Ether and parse the output to produce more meaningful information. Minereum starts an ethereum node using Geth and a standalone miner using Ethminer. Geth works in conjunction with Ethminer, using Ethminer as a worker and Geth as a scheduler.

## Features
* One command spawns all neccessary tasks
* Meaningful log messages
* Query for accounts and balances
* Average hash rate, updates on one line
* Mine on GPU or CPU
* Benchmarking

## Install
* Ensure you have installed Geth and set up an account
* Ensure you have installed Ethminer and checked it runs correctly
* Clone the repository `git clone https://github.com/CameronDiver/RunEthereumMiner.git`
* Move into the `RunEthereumMiner` directory 
* Run the command `python runminer.py -h` to view the usage options

## GPU Mining
* Run the command `minereum -G --geth="path to Geth" --ethminer="path to Ethminer`

## CPU Mining
* Run the command `minereum --geth="path to Geth" --ethminer="path to Ethminer`

## Output
```
./minereum -G --geth="../go-ethereum/build/bin/geth" --ethminer="/usr/bin/ethminer"
[22:37  info]	Running command '../go-ethereum/build/bin/geth --rpccorsdomain localhost --rpc'
[22:37  info]	Running command '/usr/bin/ethminer -G'
[22:37  ethminer]	Connecting to geth JSON... 
[22:37  ethminer]	Connected.
[22:37  ethminer]	Full DAG loaded 
[22:37  ethminer]	Average Speed: 1.798Mh/s 
```

## Query for accounts and balances
* Type 'h' whilst Minereum is running to view help
* Type 'q' whilst Minereum is running to quit
* Type 'a' whilst Minereum is running to view accounts
* Type 'b' whilst Minereum is running to view balances

## More Information
For more information on installing Geth and Ethminer take a look at the [wiki](http://ethereum.gitbooks.io/frontier-guide/content/mining.html).
To see the Ethereum network stats take a look at [stats.ethdev.com](https://stats.ethdev.com/)

