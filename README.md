Traitify  Python 2.x
==================

```
traitify = Traitify()
traitify.host = "api.traitify.com"
traitify.deck_id = "your deck id"
traitify.public_key = "your public key"
traitify.private_key = "your private key"
traitify.version = "v1"
print(traitify.create_assessment().id)
```