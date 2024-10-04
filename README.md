# Static Website Builder

This is a project that builds out a static react site based on an image of the design that you provide to OpenAI. The app leverages LLM Agent capabilities to build out the site. It showcases the following key features:

1. **Image to Website** 🖼️: The app includes processes an image and generates an index.html and index.css with the basic structure of the website. Provide an image of a static website and instruct the AI to create a plan, confirm that the plan looks good and then ask for it to implement the plan, and watch as it implements each milestone on the plan by creating html and css files and updating the files with code!

2. **Plan Generation Tracking** 📝: The app generates a plan ahead of building the site and updates the plan as each step is being implemented.

3. **Responsive Design** 📱: The app ensures that the generated website is fully responsive, adapting to different screen sizes and devices to provide an optimal user experience.

4. **OpenAI Integration** 🤖: The app is connected to OpenAI's API, allowing it to leverage state-of-the-art language models for generating responses.

5. **LLM Agents** 👩‍💻👨‍💻: The app uses LLM agents to accomplish building a site. A planning agent, takes care of creating the plan with milestones, updating the generated files (html, css), and updating the plan as each milestone is implemented. The implementation agent, takes care of writing code for each milestone and updating the files. Take a look at the prompt files to find the prompts for each agent.

6. **Streaming Responses** 📡: Instead of waiting for the entire response to be generated, the app streams the AI's response in real-time, providing a more interactive and engaging user experience.

7. **Chat History** 🗨️: The application maintains a conversation history, enabling context-aware responses and allowing for more coherent and meaningful interactions.

8. **Environment Variable Management** 🔒: Sensitive information like API keys are managed securely using environment variables.

9. **Langfuse Integration** 📊: The app includes Langfuse for tracing and monitoring AI interactions, which can be useful for debugging and optimizing your AI application.

## Getting Started

### 1. Create a virtual environment

First, create a virtual environment to isolate the project dependencies:

```bash
python -m venv .venv
```

### 2. Activate the virtual environment:

- On Windows:
  ```bash
  .venv\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

Install the project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

- Copy the `.env.sample` file to a new file named `.env`
- Fill in the `.env` file with your API keys

## Running the app

To run the app, use the following command:

```bash
chainlit run app.py -w
```

## Updating dependencies

If you need to update the project dependencies, follow these steps:

1. Update the `requirements.in` file with the new package or version.

2. Install `pip-tools` if you haven't already:

   ```bash
   pip install pip-tools
   ```

3. Compile the new `requirements.txt` file:

   ```bash
   pip-compile requirements.in
   ```

4. Install the updated dependencies:
   ```bash
   pip install -r requirements.txt
   ```

This process ensures that all dependencies are properly resolved and pinned to specific versions for reproducibility.
