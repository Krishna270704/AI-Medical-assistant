import requests

session = requests.Session()
print("Sending first query...")
res1 = session.post("http://127.0.0.1:5000/", data={"user_input": "What are the symptoms of flu?"})
print("Status 1:", res1.status_code)

print("Sending follow up query...")
res2 = session.post("http://127.0.0.1:5000/", data={"user_input": "And how do I treat it?"})
print("Status 2:", res2.status_code)

if "symptoms" in res2.text.lower() or "treat" in res2.text.lower():
    print("Memory works! Output contained references to history.")
else:
    print("Might have failed.")
