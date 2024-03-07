import os
from dotenv import load_dotenv, find_dotenv

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

_: bool = load_dotenv(find_dotenv())

SEED = "Find if the product or product's company have any of the provided eco friendly certifications. In Response tell about each asked Certification and if you are unable to find the data about any eco certification then response by telling no Data is available about that one. Keep your response consise and logical comment about each certification shall be No more than 60 words. "

tools = [TavilySearchResults(max_results=5)]

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-tools-agent")

# Choose the LLM that will drive the agent
# Only certain models support this
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def search(query: str):
    # Execute the agent
    # results = agent_executor.invoke({"input": query})
    results = agent_executor.invoke(
            {
                "input": query,
                "chat_history": [
                    SystemMessage(content=SEED),
                ],
            }
        )

    return results