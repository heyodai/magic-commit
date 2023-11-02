import os
import subprocess
import openai
import dagwood
from .config import get_api_key, set_api_key
from jinja2 import Environment, PackageLoader

log = dagwood.assemble(format='')

def get_commit_messages(directory):
    if not os.path.isdir(os.path.join(directory, '.git')):
        raise Exception("Error: The specified directory is not a Git repository.")

    # Run 'git log' to get the commit messages
    result = subprocess.run(['git', 'log', '--pretty=%B', '-n', '10'], cwd=directory, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception("Error: Unable to get commit messages. Are you in a Git repository?")
    
    return result.stdout

def generate_commit_message(commit_messages, model='gpt-3.5-turbo'):
    # Verify an API key is set
    if not get_api_key():
        raise Exception("Error: OpenAI API key not set. Use the -k flag to set your API key.")
    
    # Create a list of messages to send to the API
    openai.api_key = get_api_key()
    
    commit_messages_list = commit_messages.strip().split('\n')

    jinja = Environment(loader=PackageLoader('magic_commit', 'templates')).get_template('chat_completion.jinja')
    message = commit_messages_list[-1] if len(commit_messages_list) > 1 else commit_messages_list[0]
    rendered_template = jinja.render(message=message)

    messages = [{"role": "system", "content": rendered_template}]

    # messages.append({"role": "user", "content": f"Commit context: {commit_messages_list[-1]}\nCommit message: "})

    log.info(messages)

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    log.info(response)

    return response['choices'][0]['message']['content'].strip()



def run_magic_commit(args):
    if args.key:
        set_api_key(args.key)
        log.info("API key set successfully.")
        return

    directory = args.directory or '.'
    commit_messages = get_commit_messages(directory)

    try:
        model = args.model or 'gpt-3.5-turbo'
        commit_message = generate_commit_message(commit_messages, model)
    except Exception as e:
        log.error(e)
        return

    # log.info("Generated commit message:")
    # log.info(commit_message)
