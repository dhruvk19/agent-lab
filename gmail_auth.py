import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

HERE = Path(__file__).parent
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

flow = InstalledAppFlow.from_client_secrets_file(str(HERE / "credentials.json"), SCOPES)
creds = flow.run_local_server(port=8765, open_browser=False)
token = HERE / "token.json"
fd = os.open(token, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w") as f:
    f.write(creds.to_json())
token.chmod(0o600)
print("Signed in. Saved token.json")
