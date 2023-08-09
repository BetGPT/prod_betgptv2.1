from context_manager import get_conversation_context
from openai_api import chatgpt_completion
import os

if __name__ == "__main__":
    conversation = get_conversation_context()

    # First message flag
    first_message = True

    while True:
        user_input = input('\n\nUSER: ')
        conversation.append({'role': 'user', 'content': user_input})

        if first_message:
            response = "Welcome to BetGPT. I'm happy to provide current NFL betting odds from Fanduel Sportsbook. What game or games are you interested in today?"
            first_message = False
        else:
            response = chatgpt_completion(conversation)

        conversation.append({'role': 'assistant', 'content': response})

        print('\n\nBetGPT: %s' % response)
