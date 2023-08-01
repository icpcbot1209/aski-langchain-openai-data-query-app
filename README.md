# Aski 

Prompt your SQL database or CSV files using ChatGPT

# What is Aski?

Aski is Python software with build it web UI that lets you connect your data stored in a database or CSV file to a Langchain -> OpenAI API pipeline. Under the hood Langchain agents are used to build queries.

This software is built as practical example and as such is not well tested and will not be updated/supported in future. 
 
Feel free to copy and modify it according to your needs!


# Requirements

To run Aski you will need Python 3.11

All required libraries are listed in **requirements.txt** To install all in one go use:
```
pip3 install -r requirements.txt
```

# Adding your OpenAI API key

You can add your OpenAI API key in **config.yaml**

Example:
```
openai_api_key: 'secretapikey123456'
```

# Connecting your data sources

⚠️ **BE CAREFUL** ⚠️

Your API key and database credentials will be stored in plain text inside the config file.
___


To connect a data source you need to add new entry for it in the
**data_sources** dictionary in **config.yaml**

Example:
```
data_sources:
  positions_csv: 'data/customers.csv'
  positions_db: 'postgresql://username:password@11.12.123.145:1122/customers'
```

# Limitations
 -  As multiple prompts are sent to the OpenAI API running a lot of queries can be costly.

 - The Agents pipeline is not as straight-forward as prmopting ChatGPT directly, in some cases this leads to responses that are not full or completely wrong.
