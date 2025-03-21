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
        original_frontmatter_data = frontmatter_data.copy()  # Keep a copy of the original order
        
        # Translate title if present
        if "title" in frontmatter_data:
            english_title = frontmatter_data["title"]
            if english_title is not None and english_title not in translations:
                translated_title = translate_content(english_title, api_key, model, target_language)
                # Clean up the translated title (remove extra quotes and newlines)
                translated_title = translated_title.strip().replace('\n', ' ').replace('\r', '')
                translations[english_title] = translated_title
            if english_title is not None:
                frontmatter_data[f"title-{target_language}"] = translations[english_title]
            else:
                frontmatter_data[f"title-{target_language}"] = ""
        
        # Translate description if present
        if "description" in frontmatter_data:
            english_description = frontmatter_data["description"]
            if english_description is not None and english_description not in translations:
                translated_desc = translate_content(english_description, api_key, model, target_language)
                # Clean up the translated description (remove extra quotes and newlines)
                translated_desc = translated_desc.strip().replace('\n', ' ').replace('\r', '')
                translations[english_description] = translated_desc
            if english_description is not None:
                frontmatter_data[f"description-{target_language}"] = translations[english_description]
            else:
                frontmatter_data[f"description-{target_language}"] = ""

        # Preserve the original structure of the body for translation
        # Store the original line breaks and formatting
        body_lines = body.split('\n')
        body_structure = []
        current_paragraph = []
        
        for line in body_lines:
            if line.strip() == '':
                if current_paragraph:
                    body_structure.append(('paragraph', '\n'.join(current_paragraph)))
                    current_paragraph = []
                body_structure.append(('empty', ''))
            elif line.startswith('#'):
                if current_paragraph:
                    body_structure.append(('paragraph', '\n'.join(current_paragraph)))
                    current_paragraph = []
                body_structure.append(('heading', line))
            elif line.startswith('- ') or line.startswith('* ') or re.match(r'^\d+\. ', line):
                if current_paragraph:
                    body_structure.append(('paragraph', '\n'.join(current_paragraph)))
                    current_paragraph = []
                body_structure.append(('list_item', line))
            elif line.startswith('> '):
                if current_paragraph:
                    body_structure.append(('paragraph', '\n'.join(current_paragraph)))
                    current_paragraph = []
                body_structure.append(('quote', line))
            else:
                current_paragraph.append(line)
        
        if current_paragraph:
            body_structure.append(('paragraph', '\n'.join(current_paragraph)))

        # Clean text for translation (remove HTML, Liquid tags, etc.)
        text_only = re.sub(r'<.*?>|{%[\s\S]*?%}|{{[\s\S]*?}}', '', body)
        text_only = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text_only)
        text_only = re.sub(r'\s+', ' ', text_only)
        text_only = text_only.strip()
        
        # Translate the content
        if text_only and text_only.strip() and text_only not in translations:
            translated_content = translate_content(text_only, api_key, model, target_language)
            translations[text_only] = translated_content
        elif text_only.strip() == "":
            translations[""] = ""
        
        # Add the lang front matter
        if target_language != "en":
            frontmatter_data["lang"] = target_language

        # Rebuild the frontmatter while preserving the original order
        ordered_frontmatter = {}
        for key in original_frontmatter_data.keys():
            ordered_frontmatter[key] = frontmatter_data.get(key, original_frontmatter_data[key])
        
        # Add any new keys that weren't in the original
        for key in frontmatter_data.keys():
            if key not in ordered_frontmatter:
                ordered_frontmatter[key] = frontmatter_data[key]
        
        # Use the ordered frontmatter
        new_frontmatter = "---\n" + yaml.dump(ordered_frontmatter, allow_unicode=True, sort_keys=False) + "---\n"

        # Combine the frontmatter and translated body
        # Try to preserve the original structure as much as possible
        translated_body = translations[text_only] if text_only else body
        
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
            f.write(new_frontmatter)
            f.write(translated_body)

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
            yaml.dump(translations, f, allow_unicode=True, sort_keys=False)
        
        print(f"Successfully processed {input_file}.")
        print(f"Translations saved to {translations_file}")
    else:
        print(f"Failed to process {input_file}.")
        sys.exit(1)


if __name__ == "__main__":
    main()