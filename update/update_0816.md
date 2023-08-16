**New Integration with OpenAI 😎:**
- **Interface:** Encapsulated complete code interpreter process into an OpenAI-style interface.
- **Endpoint:** http://localhost:8000/v1/chat/completions

**Available Models 😈:**
1. `gpt-3.5-turbo-codeinterpreter`
2. `gpt-4-codeinterpreter`
3. `gpt-3.5-turbo-16k-codeinterpreter`
- **Note:** They utilize the standard OpenAI API request format and handle context automatically.

**Code Reference 🚀:**
```python
def my_print(text):
    function_name = ""
    if 'choices' in text:
        choices = text['choices']
        if len(choices) > 0 and 'delta' in choices[0]:
            delta = choices[0]['delta']
            if 'content' in delta:
                if delta['content'] != None:
                    print(delta['content'], end="", flush=True)
            if "function_call" in delta:
                if "name" in delta["function_call"]:
                    function_name = delta["function_call"]["name"]
                    print(function_name + ": " + "function_args\n", end="", flush=True)
                if "arguments" in delta["function_call"]:
                    print(delta["function_call"]["arguments"], end="", flush=True)
            if "tool" in delta and 'output' in delta:
                print(delta['output'], end="", flush=True)
            if choices[0]['finish_reason'] != None:
                print()       
```
- **More Features:** More functionalities will be added to various multi-functional models.

**New Features 😁:**
1. **Parameter Settings 🎛️:** Conveniently switch between models using left-side settings options.
![image](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/609da341-9462-4b8a-a672-99d3d1dcbc4b)
2. **Chat History 📝:** Session-based JSON file storage for chat history.
3. **Continued Conversations 🔄:** Seamless continuation of previous chats with the same `session_id`.

**Coming Soon 🛠️:**
- **Persistent Memory with Zep:** A long-term memory vision in fine-tuning. Will be released in the next version.

**Setup Instructions 😇:**
- Update chainlit with `pip install chainlit==0.6.2`
- Run the server with `chainlit run app_server.py`

**Stay Tuned! 🚀😈🔥**

![20230816204754](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/30cac958-0f4e-40b5-aa17-276e4796ee09)