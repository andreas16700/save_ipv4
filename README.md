# ⚡ Save current public IPv4 to Appwrite Cloud

I self-host an appwrite instance on my home network. I don't have a static IP which means it changes sometimes.

This function is meant to run on a regular basis on the self hosted instance.

This function fetches the current public IPv4 address from https://api.ipify.org and saves it on a database on Appwrite Cloud.



## Assumptions
There is a database (id='constants'), inside it a collection (id=`ip`) with a required IP attribute with two documents:

* `current`: the current public IPv4 address
* `old`: the previously saved IPv4 address

The above documents are updated iff the currently saved address on AW Cloud differs from the currently public IPv4 address.


## 🔒 Environment Variables



| Key               | Value                    |
|-------------------|--------------------------|
| AW_CLOUD_KEY | `the_api_key_for_aw_cloud` |
