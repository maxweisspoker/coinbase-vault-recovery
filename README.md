# coinbase-vault-recovery
Simple terminal Python app for recovering Coinbase vault keys

Only individual vaults with the user controlloing the keys can be recovered.  You must have your user seed (or master xprv key), the encrypted shared seed, all three xpub public keys, and your vault password.

Requires:  PyCrypto, scrypt, pybip38, simplebitcoinfuncs (requires pbkdf2)

If you have all of the necessary info and python software requirements, then just run the app with Python on the terminal or cmd.exe and follow the instructions it gives you.  It will provide you with the address, redeem script, and two private keys for signing.

You can use that information to make a new transaction to get your money.  I personally recommend the site Coinb.in:

https://coinb.in/#newTransaction
