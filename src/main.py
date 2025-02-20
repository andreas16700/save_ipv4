from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import os, requests

client = (
        Client()
        # .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project('latsia-support')
        .set_key(os.environ["AW_CLOUD_KEY"])
    )
databases = Databases(client)

url = "https://api.ipify.org"
DB_ID = "constants"
COLL_ID = "ip"



def fetch_public_ipv4(context):
    # Fetch the current public IPv4 address using ipify
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad status codes
        current_ip = response.text.strip()  # The API returns the IP as plain text
        context.log(f"fetched ip from {url}: {current_ip}")
        return current_ip
    except requests.RequestException as e:
        # Handle error appropriately (logging, retrying, etc.)
        context.error(f"Error fetching IP: {e}")
        return None
def get_ip(doc_id):
    return databases.get_document(database_id=DB_ID, collection_id=COLL_ID, document_id=doc_id)[
        'ipv4']
def save_ip(ip, doc_id):
    databases.update_document(database_id=DB_ID, collection_id=COLL_ID, document_id=doc_id, data={
        "ipv4": ip
    })
# This Appwrite function will be executed every time your function is triggered
def main(context):
    # You can use the Appwrite SDK to interact with other services
    # For this example, we're using the Users service

    current_ip = fetch_public_ipv4(context)
    if current_ip is None:
        exit(1)



    try:
        # keep the currently saved ip as a backup, then save the new one.

        current_saved = get_ip(doc_id="current")
        if current_saved == current_ip:
            context.log(f"current ip is the one that's saved: {current_ip}")

        save_ip(ip=current_saved, doc_id="old")

        save_ip(ip=current_ip, doc_id="current")


        # Log messages and errors to the Appwrite Console
        # These logs won't be seen by your end users
        # context.log("Total users: " + str(response["total"]))
    except AppwriteException as err:
        context.error("appwrite error: " + repr(err))
        exit(1)


    return context.res.json(
        {
            "saved_ip": current_ip,
            "old": current_saved,
        }
    )
