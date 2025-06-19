import requests

pnr_number = "6652078931"  # Replace this with your actual PNR number
url = f"https://irctc-indian-railway-pnr-status.p.rapidapi.com/getPNRStatus/{pnr_number}"

headers = {
    "X-RapidAPI-Key": "7b1feb9d45mshfe663e5c770a9cfp123036jsn5d345f3906a2",
    "X-RapidAPI-Host": "irctc-indian-railway-pnr-status.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
print(response.json())
