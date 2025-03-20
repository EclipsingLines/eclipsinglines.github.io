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
            {"role": "user", "content": "Translate the following content to Spanish, return ONLY the translated text: {content}"}
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

        # Parse the frontmatter
        frontmatter = ""
        body = ""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) == 3:
                frontmatter = parts[1].strip()
                body = parts[2].strip()
        else:
            body = content

        # Translate the title, description, and content
        frontmatter_data = yaml.safe_load(frontmatter) if frontmatter else {}
        if "title" in frontmatter_data:
            frontmatter_data["title-es"] = translate_content(frontmatter_data["title"], api_key, model, prompt)
        if "description" in frontmatter_data:
            frontmatter_data["description-es"] = translate_content(frontmatter_data["description"], api_key, model, prompt)
        translated_body = translate_content(body, api_key, model, prompt)

        # Rebuild the frontmatter
        new_frontmatter = "---\n" + yaml.dump(frontmatter_data, allow_unicode=True) + "---\n"

        # Write the translated content to the output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(new_frontmatter + translated_body)

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