import requests

url = "http://wjvqwct2gr6sx7gkgp4z2q6jhohzjdxbdwyarpfuqkzvqfzppugj2eyd.onion/"

file_path = input("Enter file path: ")

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("Server response:", response.text)
