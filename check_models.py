from google import genai

client = genai.Client(api_key="AIzaSyDKpQJYiNFGAg56HFcSYCagbMLG8yKwDSA")

print("Checking available models...")
for model in client.models.list():
    print(f"Model Name: {model.name} | Actions: {model.supported_actions}")