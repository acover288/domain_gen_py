# Domain Name Generator

The Domain Name Generator is a Python script that helps you generate domain name suggestions based on certain criteria, such as preferred name styles, business description, domain length constraints, included words, and top-level domains (TLDs) to check. The script uses both user inputs and AI-powered suggestions to provide a list of domain name options.

## Features

- Generate domain name suggestions based on user-defined criteria.
- Option to reuse previously saved inputs for rerunning the script.
- Utilizes an AI-powered function to provide creative and relevant domain name suggestions.
- Checks domain name existence for specified TLDs.

## Requirements

- Python 3.x

## Installation

1. Make sure you have Python 3.x installed on your system.

2. Install the required dependencies from the `requirements.txt` file using the following command:

   pip install -r requirements.txt

3. Create a .env file in the root directory of your project and add the following lines:

    ```makefile
    OPENAI_ORGANIZATION=your_organization_name
    OPENAI_API_KEY=your_api_key
    ```

Replace your_organization_name with your OpenAI organization name and your_api_key with your OpenAI API key.

## Usage

Run the script using the following command:

    python domain_name_generator.py

The script will interactively prompt you for input on domain name preferences, business description, domain length constraints, included words, and TLDs to check.

After providing the necessary input, the script will generate a list of domain name suggestions and check their existence for the specified TLDs.

To rerun the script with the same inputs as before, use the following command:

    python domain_name_generator.py --rerun

## Contributions

Contributions to improve and enhance the Domain Name Generator are welcome. You can fork the repository, make your changes, and create a pull request.

This project is licensed under the MIT License - see the LICENSE file for details.
