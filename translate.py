import os
import sys
import requests
import yaml

def translate_content(content, api_key, model, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Translate the following content to Spanish: {content}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    if len(sys.argv) != 5:
        print("Usage: python translate.py <input_file> <output_file> <api_key> <model>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    api_key = sys.argv[3]
    model = sys.argv[4]

    # Load the translation prompt from prompt.txt
    with open("prompt.txt", "r") as f:
        prompt = f.read().strip()

    try:
        with open(input_file, "r") as f:
            content = f.read()

        translated_content = translate_content(content, api_key, model, prompt)

        # Create the es directory if it doesn't exist
        es_dir = os.path.dirname(output_file)
        if not os.path.exists(es_dir):
            os.makedirs(es_dir)

        with open(output_file, "w") as f:
            f.write(translated_content)

        print(f"Translated content from {input_file} to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()