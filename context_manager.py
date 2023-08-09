import json
from datetime import datetime

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

def get_conversation_context():
    # Get the current date
    current_date = datetime.now().strftime('%Y_%m_%d')

    scratchpad = open_file(f'data/nfl_scratchpad_{current_date}.txt')
    system_message = open_file('data/system_prompt.txt').replace('<<INPUT>>', '')
    system_message += scratchpad
    
    conversation = [{'role': 'system', 'content': system_message}]
    return conversation