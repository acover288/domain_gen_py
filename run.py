import whois
import sys
import json

from openaiUtil import send_function_chat_completion

def domain_exists(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        if domain_info.status:
            return True
        return False
    except whois.parser.PywhoisError:
        return False

def get_user_input(prompt):
    user_input = input(prompt)
    return user_input.strip()

def get_int_input(prompt):
    input_str = get_user_input(prompt + " (leave blank for no constraint): ")
    if input_str:
        return int(input_str)
    return None

def get_multiple_inputs(prompt):
    items = []
    while True:
        item = get_user_input(prompt + " (or press Enter to finish): ")
        if not item:
            break
        items.append(item)
    return items

def generate_names(names, description, min_domain_length, max_domain_length, included_words, tlds):
    prompt = f'Please suggest at least 10 domain names that fit the following criteria:\n'
    prompt += f'For a business doing: ###{description}###' if description else ""
    prompt += f'Similar in style to: ###{", ".join(names)}###' if names else ""
    prompt += f'With a minimum length of: {min_domain_length}' if min_domain_length else ""
    prompt += f'With a maximum length of: {max_domain_length}' if max_domain_length else ""
    prompt += f'Include the following words: {", ".join({included_words})}' if included_words else ""
    prompt += f'Consider these tlds: {", ".join({tlds})}' if included_words else ""

    functions = [
        {
            "name": "suggest_domains",
            "description": "Suggests a list of domains that fits the above criteria",
            "parameters": {
                "type": "object",
                "properties": {
                    "domains": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "The suggested domain without the tld"},
                                "tld": {"type": "string", "description": "The best tld"},
                                "explain": {"type": "string", "description": "A justification for why this domain is a good suggestion"},
                            },
                            "required": [
                                "domain",
                                "explain",
                                "tld",
                            ]
                        }
                    }
                },
                "required": ["wordLevels"]
            }
        }
    ]

    result = send_function_chat_completion(prompt, functions, temperature=1)
    return result['domains']

def save_inputs_to_json(inputs):
    with open("inputs.json", "w") as json_file:
        json.dump(inputs, json_file, indent=4)

def load_inputs_from_json():
    try:
        with open("inputs.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def main():
    print("Welcome to the Domain Name Generator!")

    if len(sys.argv) > 1 and sys.argv[1] == "--rerun":
        saved_inputs = load_inputs_from_json()
        names = saved_inputs.get("names", [])
        description = saved_inputs.get("description", "")
        min_domain_length = saved_inputs.get("min_domain_length")
        max_domain_length = saved_inputs.get("max_domain_length")
        included_words = saved_inputs.get("included_words", [])
        tlds = saved_inputs.get("tlds", [])
    else:
        names = get_multiple_inputs("Enter a name you like the style of")
        description = get_user_input("Enter a description of the business: ")
        min_domain_length = get_int_input("Enter the minimum length of the domain name")
        max_domain_length = get_int_input("Enter the maximum length of the domain name")
        included_words = get_multiple_inputs("Enter a word that must be included in the domain name")
        tlds = get_multiple_inputs("Enter a top level domain (TLD) to check")

    inputs = {
            "names": names,
            "description": description,
            "min_domain_length": min_domain_length,
            "max_domain_length": max_domain_length,
            "included_words": included_words,
            "tlds": tlds
        }
    save_inputs_to_json(inputs)

    generated_domains = generate_names(names, description, min_domain_length, max_domain_length, included_words, tlds)

    for suggestion in generated_domains:
        print(f'{suggestion["domain"]} - {suggestion["explain"]}')
        for tld in (tlds or ['com']):
            domain = suggestion["domain"] + "." + tld
            exists = "Exists" if domain_exists(domain) else "Doesn't Exist"
            print(f'{domain} - {exists}')
    
    print("To rerun with the same inputs, run the script with arguments --rerun")

if __name__ == "__main__":
    main()
