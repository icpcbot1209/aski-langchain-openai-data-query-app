import gradio as gr
import pandas as pd
from . import defaults
from traceback import format_exc
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, create_sql_agent, create_pandas_dataframe_agent


class Chat:
    def __init__(self, data_sources: dict):
        self.data_sources = data_sources
        self.active_data_source: str = ''
        self.agents = {}

    def get_agent(self) -> AgentExecutor:
        '''
        Checks if an agent for the currently active data source already exists in the agents dict. 
        If not creates it, then returns the agent.
        '''
        if self.active_data_source not in self.agents:
            # CSV agent
            if self.data_sources[self.active_data_source].endswith('csv'):
                df = pd.read_csv(self.data_sources[self.active_data_source])
                self.agents[self.active_data_source] = create_pandas_dataframe_agent(
                    llm=OpenAI(temperature=0.1),
                    df=df,
                    verbose=True,
                    include_df_in_prompt=False, 
                    max_iterations=15
                )
            # SQL database agent
            else:
                self.agents[self.active_data_source] = create_sql_agent(
                    llm=OpenAI(temperature=0.1),
                    toolkit=SQLDatabaseToolkit(
                        db=SQLDatabase.from_uri(self.data_sources[self.active_data_source]), 
                        llm=OpenAI(temperature=0.1)
                    ),
                    verbose=True,
                    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    max_iterations=15
                )
        
        return self.agents[self.active_data_source]
        
    def respond(self, message: str, chat_history: list):
        '''
        Generates a response to a message and updates the chat history.
        '''
        try:
            agent = self.get_agent()
            response = agent.run(message)
            chat_history.append((message, response))
        except:
            response = f"Loading file failed: \n```\n{format_exc(1, False)}\n```"
            chat_history.append((message, response))
        
        return "", chat_history
    
    def data_source_select(self, value: str):
        '''Gets called when data source is selected from the dropdown menu'''
        self.active_data_source = value
    
    def launch(self):
        '''Will be called when the app is started'''
        
        # Setup the colors of the UI
        accent_color = gr.themes.colors.Color(
            name=defaults.app_name,
            c50=defaults.accent_color_light,
            c100=defaults.accent_color_dark,
            c200=defaults.accent_color_dark,
            c300=defaults.accent_color_dark,
            c400=defaults.accent_color_dark,
            c500=defaults.accent_color_light,
            c600=defaults.accent_color_dark,
            c700=defaults.accent_color_dark,
            c800=defaults.accent_color_dark,
            c900=defaults.accent_color_dark,
            c950=defaults.accent_color_dark,
        )
        # Setup the text size of the UI
        text_size = gr.themes.Size(
            name=defaults.app_name,
            **defaults.text_sizes
        )
        
        # The app is using the Monochrome theme with updated primary color and text size
        theme = gr.themes.Monochrome(primary_hue=accent_color, text_size=text_size)
        
        with gr.Blocks(theme=theme, title=defaults.app_name, analytics_enabled=False) as app:
            # Dropdown menu
            data_source_selector = gr.inputs.Dropdown(choices=self.data_sources.keys(), label='Data source')
            data_source_selector.select(fn=self.data_source_select, inputs=data_source_selector)
            
            # Chat box
            chatbot = gr.Chatbot(show_label=False, height=defaults.chat_box_height)
            
            # Input text box
            msg = gr.Textbox(show_label=False, autofocus=True, placeholder=defaults.text_box_placeholder)
            msg.submit(self.respond, [msg, chatbot], [msg, chatbot])
        
        app.launch(show_api=False)
