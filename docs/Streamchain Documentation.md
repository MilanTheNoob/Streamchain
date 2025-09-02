# Streamchain
Streamchain is a prototype blockchain running on caffiene and copium.

It is composed of the:

- [[Streamchain Documentation Miner|miner]] - stores the state of the chain & provides a flask server to change said state
- [[Streamchain Documentation Desktop Client|desktop client]] - a windows-based (for now) client used to watch & create streams

In the future, it is expected to have:

- CLI support built into the desktop client
- A rust based implementation of the miner for *speed*
- A web-based package to enable web applications to interact the chain (I mean wouldn't it be cool to have a decentralized twitch?)