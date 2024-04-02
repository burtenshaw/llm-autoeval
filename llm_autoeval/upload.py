import os
import requests

from huggingface_hub import ModelCard

def upload_to_github_gist(text, gist_name, gh_token):
    # Create the gist content
    gist_content = {
        "public": str(os.getenv("PRIVATE_GIST", False)).lower(),
        "files": {
            f"{gist_name}": {  # Change the file extension to .txt for plain text
                "content": text
            }
        },
    }

    # Headers for the request
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Make the request
    response = requests.post(
        "https://api.github.com/gists", headers=headers, json=gist_content
    )

    if response.status_code == 201:
        print(f"Uploaded gist successfully! URL: {response.json()['html_url']}")
    else:
        print(
            f"Failed to upload gist. Status code: {response.status_code}. Response: {response.text}"
        )


def upload_to_hf_model_repo(text, model_id):
    hf_token = os.getenv("HF_TOKEN")
    model_name = model_id.split("/")[-1]
    
    # Create model card
    card = ModelCard.load(model_id)
    card.content += "--- \n" + text
    card.save(f'{model_name}/README.md')
    card.push_to_hub(token=hf_token)