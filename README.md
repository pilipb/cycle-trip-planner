# Cycle Trip Planner
Agent to plan cycling trips. Agent has access to a real route planning API and mock data w.r.t. accomodation, weather etc.

## Demo

![Cycle Planner Demo](cycle-planner-demo.mp4)

## How to run locally

Prerequisite
- Python 3.x, Node 18+ (if using UI)

First create venv with:
```python -m venv venv```

activate this virtual environment:
```source venv/bin/activate```

install requirements
```pip install -r requirements.txt```

add your api keys to a .env in the root:
```ANTHROPIC_API_KEY=```
```OPENROUTE_SERVICE_API_KEY=``` (get a free key at https://openrouteservice.org/dev/#/signup)

then you can either run locally as a cli - chat through the terminal:
```python cli.py```

or open up the web app:

in one terminal open the next app
```cd cycle-planner```
```npm i``` to install packages
```npm run dev```

in another terminal startup the agent server
```python -m src.api.main```

open the ui in the local next js application 
e.g. http://localhost:3000 


## Architecture decisions

The big architectural decision is using Pydantic AI agent framework - I've worked with this before and found it simple to set up with plenty of space for complexity. The main agent context and chat loop are handled by the pydantic agent class. I have used `tool_plain` for the tools as the context being passed into the tools can be derived by the agent as parameters to the tools rather than passing the whole context in. Where the tools are more complicated e.g. llm calls there may need to be more context and i would then use the `.tool` rather than `.tool_plain` type. Each llm response is actioned by `run_stream_events` (streaming equivalent of run_sync - like a completion) in the pydantic ai module.

The endpoint uses SSE for streaming with a single endpoint for both new and continued messages. Allows for both thinking and text and question events to be streamed. This is mainly done so that the user has feedback while using the product - and makes it a more pleasant answering experience.

Next big decision is using the deferred tool calls, using pydantics `CallDeferred` to pause the agent execution and request an input. This is instead of doing extra turns on the agent it just continues from that exact point - so reduces round trips (and tokens) while still allowing inputs and also so that the user can have multiple choice responses so make it quicker process.

In terms of managing the conversation over the course of multiple messages, I've used a simple dictionary at the module level that keys messages by session id. This is handled in `agent/session.py` This memory is volatile and very simple - if i were to deploy this service, the session and message management would be handle within a DB.

Orchestration is prompt driven, the system prompt defines what the typical tool call sequence should be, and what should happen if user answers change. I've injected todays date so that there is better accuracy in terms of time based recommendations.

The frontend / backend choice is nextjs communicating with the python fastapi server - this is chosen purely for quickest UI implementation, it's very clean and gives a sense of the UX and easy to host.

Tools are separated by area of responsibility, with `tools/route.py` being an example of a more thoroughly developed set of tools all related to geo information. 

Finally theres an interesting point to be made about the GeoJSON flow, while the agent has access to the route planning api which returns a GeoJSON object, this object is never handled by the actual agent model (and doesn't go into the model context). It sits in the session store instead and it is returned directly to the api. The reasoning here is that the object is way too large and would likely take many tokens thereby either breaking the response of clogging the context.


## Whats next

From the tech side:
1. Replace the mock tools with real APIs, or give the agent web search as a tool for weather etc.
2. Proper session persistence using a database.
3. Do day by day map break down with more waypoints and poi visually shown on map
4. Auth on the apis - hasnt been added as this is not designed to be deppooyed, but prior to publication x-api-key or jwt auth should be added to the api routes to ensure that the agent cannot be abused. Similarly would need to change CORS to not allow ALL origins.

From product side:
1. This is likely being used as a brainstorm partner so i think centering the UI around the map and interactive use of the map would be best. Where users can manually select way points on the map and the agent updates in the background
2. NextJS is great for an mvp but this would likely be aimed at users on mobile so potentially a native front end - similar to the komoot app.
3. while the output makes sense i think the real value of this product would be in how it connects to existing tools, hence why i added the gpx export, and how it copes with live updates through a map based ui. The goal being to provide the value of a trip planner - live.
