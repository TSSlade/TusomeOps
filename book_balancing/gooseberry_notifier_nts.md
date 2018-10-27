# Notes to self for Gooseberry Notifier

Per discussion with Mike McKay, we've got a couple different approaches we can take.

1. **The "Hacky" Approach:** Run the same cURL query we use to pull Gooseberry data down for other purposes on some regular schedule. Store the result in a view or temporary data frame or something (PrevQuery). Run a new query at some time point _x_ thereafter (NewQuery). Diff the two, saving the delta (Message). _Message_ gets transmitted to the recipients (Bruce et al), NewQuery overwrites PrevQuery. We wait until the next scheduled time to run the cURL query, and fire it again. Lather, rinse, repeat.
2. **The Elegant Way:** Build a "watcher" that sits on top of the CouchDB instance and monitors the _changes_ feed. It's perpetually up, but just sits there silently until something initiates a change in CouchDB. When a change is fired, it looks at the event log and determines whether the change belongs to a question set we care about. If it does, it takes the next step. If it does not, it sits silently.

In the elegant case, we'd also need to think carefully about what we do next. Does it make sense to _immediately_ notify the Admin team? Or does it make sense to sit on the event until some later point (say, 6:30 AM the next day)? The tradeoffs here relate to Admins' attention and the opportunity cost of being asked to pay attention throughout the day (or proactively hunt down all fired messages at a later date) versus knowing that whatever they see when they come to the office in the morning is all they need to deal with.

The watcher script could be written in any language we want. It may make sense to use the PouchDB (JavaScript-based) approach, as it is well documented _and_ I could use the experience with JS ahead of the w209 course in MIDS.

+ [Here](https://pouchdb.com/api.html#changes) is a page of information on how the PouchDB events listener works.
+ [Here](https://couchdb-python.readthedocs.io/en/latest/client.html#database) is a page on how the CouchDB-Python library works.
+ [This](http://gooseberry.tangerinecentral.org:5984/gooseberry/_changes) is the link to the Gooseberry _changes_ feed.
+ [This](http://gooseberry.tangerinecentral.org:5984/_utils/) is the back-end view to the Gooseberry DB.

Note to self - Mike also talked about the use of [`npx`](https://www.npmjs.com/package/npx) as a tool to run Node packages remotely without needing to install them locally. We may not have a specific use case for this _right now_, but worth noting for future reference.
