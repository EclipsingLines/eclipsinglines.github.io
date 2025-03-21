import os
import sys
import requests
import yaml
import re

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


def process_file(input_file, target_language, api_key, model, translations):
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
            english_title = frontmatter_data["title"]
            if english_title is not None and english_title not in translations:
                translations[english_title] = translate_content(english_title, api_key, model, target_language)
            if english_title is not None:
                frontmatter_data[f"title-{target_language}"] = translations[english_title]
            else:
                frontmatter_data[f"title-{target_language}"] = ""
        if "description" in frontmatter_data:
            english_description = frontmatter_data["description"]
            if english_description is not None and english_description not in translations:
                translations[english_description] = translate_content(english_description, api_key, model, target_language)
            if english_description is not None:
                frontmatter_data[f"description-{target_language}"] = translations[english_description]
            else:
                frontmatter_data[f"description-{target_language}"] = ""

        # Remove HTML and Liquid tags, HTML entities, and clean up whitespace
        # First, remove HTML and Liquid tags
        text_only = re.sub(r'<.*?>|{%[\s\S]*?%}|{{[\s\S]*?}}', '', body)
        # Remove HTML entities
        text_only = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text_only)
        # Replace multiple newlines with a single newline
        text_only = re.sub(r'\n+', '\n', text_only)
        # Replace multiple spaces with a single space
        text_only = re.sub(r'\s+', ' ', text_only)
        # Strip leading and trailing whitespace
        text_only = text_only.strip()

        # Debug print
        print(f"text_only: '{text_only}'")
        
        if text_only and text_only.strip() and text_only not in translations:
            translations[text_only] = translate_content(text_only, api_key, model, target_language)
        elif text_only.strip() == "":
            # If text_only is empty, use an empty string as the key
            translations[""] = ""
        
        # Debug print
        print(f"translations keys: {list(translations.keys())}")
        
        # Add the lang front matter
        if target_language != "en":
            frontmatter_data["lang"] = target_language

        # Rebuild the frontmatter
        new_frontmatter = "---\n" + yaml.dump(frontmatter_data, allow_unicode=True) + "---\n"

        # Combine the frontmatter and body
        new_content = new_frontmatter + (translations[text_only] if text_only else body)

        # Define output_file based on input_file and target_language
        if target_language != "en":
            input_dir = os.path.dirname(input_file)
            filename = os.path.basename(input_file)
            output_dir = os.path.join(input_dir, target_language)
            output_file = os.path.join(output_dir, filename)
        else:
            output_file = input_file

        # Write the translated content to the output file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Translated content saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        return False


def main():
    if len(sys.argv) != 6:
        print(f"Error: Expected 6 arguments, but got {len(sys.argv)}.")
        print(f"Received arguments: {sys.argv}")
        print("Usage: python translate.py <input_folder> <target_language> <api_key> <model> <input_file>")
        sys.exit(1)

    input_folder = sys.argv[1]
    if not os.path.isdir(input_folder):
        print(f"Error: {input_folder} is not a directory.")
        sys.exit(1)
    target_language = sys.argv[2]
    api_key = sys.argv[3]
    model = sys.argv[4]
    input_file = sys.argv[5]  # This is the specific file to translate, not an output file

    # Create _i18n directory if it doesn't exist
    os.makedirs("_i18n", exist_ok=True)
    translations_file = f"_i18n/{target_language}.yml"
    
    # Load existing translations from the YAML file if it exists
    translations = {}
    if os.path.exists(translations_file):
        try:
            with open(translations_file, "r", encoding="utf-8") as f:
                existing_translations = yaml.safe_load(f)
                if existing_translations:
                    translations = existing_translations
        except Exception as e:
            print(f"Error loading existing translations: {e}")
    
    # Process the specified file
    print(f"Processing {input_file}...")
    
    if process_file(input_file, target_language, api_key, model, translations):
        # Write the updated translations to the YAML file
        with open(translations_file, "w", encoding="utf-8") as f:
            yaml.dump(translations, f, allow_unicode=True)
        
        print(f"Successfully processed {input_file}.")
        print(f"Translations saved to {translations_file}")
    else:
        print(f"Failed to process {input_file}.")
        sys.exit(1)


if __name__ == "__main__":
    main()