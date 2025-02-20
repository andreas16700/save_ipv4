# ⚡ Save current public IPv4 to Appwrite Cloud and update Cloudflare DNS records 

I self-host an appwrite instance on my home network. I don't have a static IP which means it changes sometimes.

This function is meant to run on a regular basis on the self hosted instance.

If the public IP changes, this function saves this on appwrite cloud, as well as updates the DNS records on cloudflare (the ones that point to the old public IPv4 address)

This function fetches the current public IPv4 address from https://api.ipify.org and saves it on a database on Appwrite Cloud.



## Assumptions
There is a database (id='constants'), inside it a collection (id=`ip`) with a required IP attribute with two documents:

* `current`: the current public IPv4 address
* `old`: the previously saved IPv4 address

The above documents are updated iff the currently saved address on AW Cloud differs from the currently public IPv4 address.


## 🔒 Environment Variables



| Key          | Value                      |
|--------------|----------------------------|
| AW_CLOUD_KEY | `the_api_key_for_aw_cloud` |
| CF_KEY       | `cloudflare_api_key`       |
| CF_TOKEN     | `cloudflare_api_token`     |
| CF_ZONE      | `cloudflare_zone_id`       |
| CF_EMAIL     | `cloudflare_account_email` |

*The cloudflare token must have edit permission for DNS records on the specified zone.*