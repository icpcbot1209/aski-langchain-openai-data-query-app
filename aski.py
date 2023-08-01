import os
import yaml
from lib import chat

if __name__ == '__main__':
    # Load the config file
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Set the OPENAI_API_KEY environment variable
    os.environ['OPENAI_API_KEY'] = config['openai_api_key']
    
    # Initiate chat
    ch = chat.Chat(data_sources=config['data_sources'])
    
    # Launch app
    ch.launch()
