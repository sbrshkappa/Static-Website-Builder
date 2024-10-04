import os
import json
import chainlit as cl

class Agent:
    """
    Base class for all agents.
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "updateArtifact",
                "description": "Update an artifact file which is HTML, CSS, or markdown with the given contents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "The name of the file to update.",
                        },
                        "contents": {
                            "type": "string",
                            "description": "The markdown, HTML, or CSS contents to write to the file.",
                        },
                    },
                    "required": ["filename", "contents"],
                    "additionalProperties": False,
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "callAgent",
                "description": "Instantiates an agent with a given name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_name": {
                            "type": "string",
                            "description": "The name of the Agent to instantiate. As of now, the only available agent is implementation_agent.",
                        }
                    },
                    "required": ["agent_name"],
                    "additionalProperties": False,
                },
            }
        }
    ]

    def __init__(self, name, client, prompt="", agents={} , gen_kwargs=None):
        self.name = name
        self.client = client
        self.prompt = prompt
        self.gen_kwargs = gen_kwargs or {
            "model": "gpt-4o",
            "temperature": 0.2
        }
        self.agents = agents
        print("DEBUG => Agent Instantiated:", self.name)
        print("DEBUG: Available Agents:", self.agents)

    async def execute(self, message_history):
        """
        Executes the agent's main functionality.

        Note: probably shouldn't couple this with chainlit, but this is just a prototype.
        """
        copied_message_history = message_history.copy()

        # Check if the first message is a system prompt
        if copied_message_history and copied_message_history[0]["role"] == "system":
            # Replace the system prompt with the agent's prompt
            copied_message_history[0] = {"role": "system", "content": self._build_system_prompt()}
        else:
            # Insert the agent's prompt at the beginning
            copied_message_history.insert(0, {"role": "system", "content": self._build_system_prompt()})

        response_message = cl.Message(content="")
        await response_message.send()

        print("-----------------DEBUG-------------------------")
        print("Executing Agent:", self.name)
        print("Available Agents:", self.agents)
        print("Message History first and last message: ", copied_message_history[0], "\n\n\n", copied_message_history[-1])
        print("---------------------------------------------------")

        stream = await self.client.chat.completions.create(messages=copied_message_history, stream=True, tools=self.tools, tool_choice="auto", **self.gen_kwargs)

        function_calls = []
        function_name = ""
        arguments = ""
        async for part in stream:
            if part.choices[0].delta.tool_calls:
                for tool_call in part.choices[0].delta.tool_calls:
                    if tool_call.index is not None:
                        while len(function_calls) <= tool_call.index:
                            function_calls.append({"name": "", "arguments": ""})
                        if tool_call.function.name:
                            function_calls[tool_call.index]["name"] += tool_call.function.name
                        if tool_call.function.arguments:
                            function_calls[tool_call.index]["arguments"] += tool_call.function.arguments
        
            if token := part.choices[0].delta.content or "":
                await response_message.stream_token(token)        
        
        for function_call in function_calls:
            function_name = function_call["name"]
            arguments = function_call["arguments"]

            print("-------------DEBUG---------------------------------------------")
            print("DEBUG: function_name:")
            print("type:", type(function_name))
            print("value:", function_name)
            print("DEBUG: arguments:")
            print("type:", type(arguments))
            print("value:", arguments)
            print("--------------------------------------------------------------")
            
            if function_name == "updateArtifact":
                
                arguments_dict = json.loads(arguments)
                filename = arguments_dict.get("filename")
                contents = arguments_dict.get("contents")

                print("------DEBUG: Updating File:", filename)
                
                if filename and contents:
                    os.makedirs("artifacts", exist_ok=True)
                    with open(os.path.join("artifacts", filename), "w") as file:
                        file.write(contents)
                    
                    # Add a message to the message history
                    message_history.append({
                        "role": "system",
                        "content": f"The artifact '{filename}' was updated."
                    })

                    stream = await self.client.chat.completions.create(messages=message_history, stream=True, **self.gen_kwargs)
                    async for part in stream:
                        if token := part.choices[0].delta.content or "":
                            await response_message.stream_token(token)

            elif function_name == "callAgent":

                arguments_dict = json.loads(arguments)
                agent_name = arguments_dict.get("agent_name")
                print(self.name, "is calling Agent =>", agent_name)
                print("DEBUG: Available Agents:", self.agents)
                print("DEBUG: This agent's Prompt is: \n", self.prompt)
                if agent_name and agent_name in self.agents:
                    await self.agents[agent_name].execute(copied_message_history)

        else:
            print("No tool call")

        await response_message.update()

        return response_message.content

    def _build_system_prompt(self):
        """
        Builds the system prompt including the agent's prompt and the contents of the artifacts folder.
        """
        artifacts_content = "<ARTIFACTS>\n"
        artifacts_dir = "artifacts"

        if os.path.exists(artifacts_dir) and os.path.isdir(artifacts_dir):
            for filename in os.listdir(artifacts_dir):
                file_path = os.path.join(artifacts_dir, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        file_content = file.read()
                        artifacts_content += f"<FILE name='{filename}'>\n{file_content}\n</FILE>\n"
        
        artifacts_content += "</ARTIFACTS>"

        return f"{self.prompt}\n{artifacts_content}"