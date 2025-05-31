from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import os, requests, json
from datetime import datetime
from cloudflare import Cloudflare
from cloudflare.types.dns.batch_patch_param import ARecord
from dotenv import load_dotenv

def custom_serializer(obj):
    if isinstance(obj, datetime):
        # Convert datetime to an ISO-formatted string
        return obj.isoformat()
    if hasattr(obj, '__dict__'):
        # For other objects, use their __dict__ attribute
        return obj.__dict__
    raise TypeError(f"Type {type(obj)} not serializable")


# Determine the absolute path of the directory containing this script.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the .env file.
dotenv_path = os.path.join(script_dir, '.env')

load_dotenv(dotenv_path)

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


AW_CLOUD_KEY=os.environ["AW_CLOUD_KEY"]
CF_TOKEN = os.environ["CF_TOKEN"]
CF_KEY = os.environ["CF_KEY"]
CF_EMAIL = os.environ["CF_EMAIL"]
CF_ZONE = os.environ["CF_ZONE"]

client = Cloudflare(
    api_email=CF_EMAIL,
    api_key= CF_KEY,
    api_token=CF_TOKEN,
)
def update_dns_records(oldip: str, newip: str):
    # get all records
    page = client.dns.records.list(zone_id=CF_ZONE)
    # filter the ones pointing to the old ip
    records_of_interest = [r for r in page.result if r.content == oldip]
    if len(records_of_interest) <= 0:
        print(f"No records on cloudflare that point to the old ip: {oldip}!")
    else:
        print(f"will update {len(records_of_interest)} records on cloudflare that point to {oldip}!:")
        t = ", ".join([r.name for r in records_of_interest])
        print(t)
    # update those
    try:
        response = client.dns.records.batch(zone_id=CF_ZONE, patches=[ARecord(id=re.id, content=newip) for re in records_of_interest])
        print(json.dumps(response, default=custom_serializer, indent=5))
    except Exception as e:
        print(f"error updating dns records: {e}")


def fetch_public_ipv4():
    # Fetch the current public IPv4 address using ipify
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad status codes
        current_ip = response.text.strip()  # The API returns the IP as plain text
        print(f"fetched ip from {url}: {current_ip}")
        return current_ip
    except requests.RequestException as e:
        # Handle error appropriately (logging, retrying, etc.)
        print(f"Error fetching IP: {e}")
        return None
def get_ip(doc_id):
    return databases.get_document(database_id=DB_ID, collection_id=COLL_ID, document_id=doc_id)[
        'ipv4']
def save_ip(ip, doc_id):
    databases.update_document(database_id=DB_ID, collection_id=COLL_ID, document_id=doc_id, data={
        "ipv4": ip
    })

if __name__ == '__main__':

    current_ip = fetch_public_ipv4()
    if current_ip is None:
        exit(1)

    try:
        # keep the currently saved ip as a backup, then save the new one.

        current_saved = get_ip(doc_id="current")
        if current_saved == current_ip:
            msg = f"current ip is the one that's saved: {current_ip}"
            print(msg)
            exit(0)
        print(f"saving new ip {current_ip} and old ip {current_saved}")
        save_ip(ip=current_saved, doc_id="old")

        save_ip(ip=current_ip, doc_id="current")

        print(f"done!")

        print(f"updating cloudflare records...")
        update_dns_records(oldip=current_saved, newip=current_ip)


        # Log messages and errors to the Appwrite Console
        # These logs won't be seen by your end users
        # context.log("Total users: " + str(response["total"]))
    except AppwriteException as err:
        print("appwrite error: " + repr(err))
        exit(1)


    exit(0)