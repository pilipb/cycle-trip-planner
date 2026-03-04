# cycle-trip-planner
Agent to plan cycling trip


## How to run locally

First create venv with:
`python -m venv venv`

activate this virtual environment:
`source venv/bin/activate`

install requirements
`pip install -r requirements.txt`

add your api key to a .env in the route
`ANTHROPIC_API_KEY=`

then you can either run locally as a cli - chat through the terminal:
`python cli.py`

or open up the web app:

in one terminal open the next app
`cd cycle-planner`
`npm i` to install packages
`npm run dev`

in another terminal startup the agent server
`python -m src.api.main`

open the ui in the local next js application 
e.g. http://localhost:3000 


## Architecture decisions

The big architectural decision is using Pydantic AI agent framework - I've worked with this before and found it simple to set up with plenty of space for complexity. The main agent context and chat loop are handled by the pydantic agent class. I have used tool_plain for the tools as the context being passed into the tools can be derived by the agent as parameters to the tools rather than passing the whole context in. Where the tools are more complicated e.g. llm calls there may need to be more context and i would then use the .tool rather than .tool_plain type.



## Whats next