import os
import sys
import requests
import yaml

def translate_content(content, api_key, model, target_language):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"Translate the following content to {target_language}, return ONLY the translated text:"
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error during API request: {e}")
        print(f"Response content: {e.response.content.decode()}")  # Print the response content for debugging
        raise  # Re-raise the exception to be caught in main()


def main():
    if len(sys.argv) != 6:
        print("Usage: python translate.py <input_file> <target_language> <api_key> <model> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    target_language = sys.argv[2]
    api_key = sys.argv[3]
    model = sys.argv[4]
    output_file = sys.argv[5]

    # Load the translation prompt from prompt.txt
    # with open("prompt.txt", "r") as f:
    #     prompt = f.read().strip()

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

        # Load existing translations from the YAML file
        translations_file = f"_data/translations/{target_language}.yml"
        if os.path.exists(translations_file):
            with open(translations_file, "r", encoding="utf-8") as f:
                translations = yaml.safe_load(f) or {}
        else:
            translations = {}

        # Translate the title, description, and content
        frontmatter_data = yaml.safe_load(frontmatter) if frontmatter else {}
        if "title" in frontmatter_data:
            english_title = frontmatter_data["title"]
            if english_title not in translations:
                translations[english_title] = translate_content(english_title, api_key, model, target_language)
            frontmatter_data["title-es"] = translations[english_title]
        if "description" in frontmatter_data:
            english_description = frontmatter_data["description"]
            if english_description not in translations:
                translations[english_description] = translate_content(english_description, api_key, model, target_language)
            frontmatter_data["description-es"] = translations[english_description]

        if body not in translations:
            translations[body] = translate_content(body, api_key, model, target_language)
        translated_body = translations[body]

        # Rebuild the frontmatter
        new_frontmatter = "---\n" + yaml.dump(frontmatter_data, allow_unicode=True) + "---\n"

        # Write the translated content to the output file
        # with open(output_file, "w", encoding="utf-8") as f:
        #     f.write(new_frontmatter + translated_body)

        # Write the updated translations to the YAML file
        with open(translations_file, "w", encoding="utf-8") as f:
            yaml.dump(translations, f, allow_unicode=True)

        print(f"Translated content from {input_file} to {translations_file}")

    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        pass


if __name__ == "__main__":
    main()