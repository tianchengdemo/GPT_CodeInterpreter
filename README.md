# GPT_CodeInterpreter Project 🤖

GPT_CodeInterpreter is an AI-driven project designed to carry out various tasks related to code interpretation. It is built on a plugin architecture that can easily extend new features.

📢 **Announcement!**

> 🎉 **I'm thrilled to announce that our open-source project now has its own reverse endpoint. We invite everyone to join the testing phase. Once testing stabilizes, we will open-source the corresponding stable features into this project.**

🌐 **Website**: [https://web.chatboxapp.xyz/](https://web.chatboxapp.xyz/)
   - 🖱️ Click the settings button in the bottom right corner
   - 🧠 Select "OPENAI API" as the AI Model Provider
   - 🔧 Change the API HOST (ensure no trailing slashes at the end)
   - 🔑 Obtain the OPENAI API KEY via [https://chat.chatify.me](https://chat.chatify.me)

Our reverse endpoint is not only supported on this website but also compatible with any applications that allow modification of the reverse endpoint, such as ChatGPT-Next-Web, etc. You can use our endpoint in the same way as you would with the official API.


🚀 **Our Reverse Endpoint Supports**:
1. 🗨️ Chatting with ChatGPT (triggers other functions, not for regular Q&A)
2. 📤 File Uploading (type '/upload'; click "CLICK TO UPLOAD")
3. 🐍 Python Code Interpreter (triggered for specific scenarios)
4. 🎨 Image Generation (testing; using stable diffusion xl and kandinsky models to generate one image each, $0.006 per generation, cost covered; seeking free alternatives)
5. 📸 Image Description (textual descriptions for images)
6. 🔍 Web Search Functionality (in testing phase)

Enjoy these exciting new features! 🎉

Discord: https://discord.gg/EBKu4CfV
Github: https://github.com/boyueluzhipeng/GPT_CodeInterpreter
微信群二维码: ![WechatIMG354](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/73426c99-4d6b-491b-8e7e-521badc4a5c9)


## Update Log 📝

Our update logs are stored in the [update](./update/) directory. You can click on the links below to view specific updates:
- [Update from August 25, 2023](./update/update_0825.md) 🆕🔥
- [Update from August 16, 2023](./update/update_0816.md)
![image](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/609da341-9462-4b8a-a672-99d3d1dcbc4b)
- [Update from August 1, 2023](./update/update_0801.md) 
- [Update from July 30, 2023](./update/update_0730.md)

Please check back regularly for our latest updates!



# Welcome to my project! 👋
I'm glad to introduce you to a project I've been working on. It's a chatbot hosted at [this link](https://chat.zhipenglu.repl.co). 

## How to Use 📚
To get started, visit the [https://chat.zhipenglu.repl.co](https://chat.zhipenglu.repl.co) and type in your query or command. Here are some commands you can use:
- **/set_api_key** - Set your OPENAI_API_KEY 🔑
- **/set_model** - Set your OPENAI_MODEL 🤖
- **/set_language** - Set your language 🌍
- **/set_api_base** - Set your OPENAI_API_BASE 🌐
- **/help** - Show this help 📘

## Enjoy! 🎉
I hope you find this chatbot useful and fun to use. Enjoy!

## 📣 Feedback & Support

🔧 **Test Website Status:** The test website is hosted on Replit and was set up in a hurry. As such, it might experience occasional downtime or restarts. Rest assured, I'm actively working on improving its stability over time.

📬 **Encountered an Issue?** If the test website is down or if you encounter any issues, please don't hesitate to [open an issue](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/issues). I'll do my best to address it as promptly as possible.

💡 **Suggestions or Feedback?** Your thoughts matter! If you have any suggestions or feedback, I'm all ears. Please share your ideas by [opening an issue](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/issues). I strive to respond and incorporate valuable feedback as quickly as I can.

Thank you for your understanding and support! 🙏



## Pictures About GPT_CodeInterpreter

![20230726150533](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/dabdf91f-0fc7-4794-bcdf-033f3e2dbafa)

![image](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/c5fac81b-7bbf-4bb8-83fe-4a0423eb3f86)

![image](https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/ce360bb1-1347-4a96-a345-d15ddef618c2)



## Video Demonstrations 🎥

https://github.com/boyueluzhipeng/GPT_CodeInterpreter/assets/39090632/d55503f7-f51c-4d0a-a284-e811eb5a98ac




## Project Features

- **Plugin Architecture**: GPT_CodeInterpreter uses a flexible and extensible plugin architecture. Each plugin is a folder containing `functions.py` and `config.json` files, defining the functionality and configuration of the plugin.

### 🌟 Upcoming Features:

- **Official Plugin Integration🔌**: By processing the provided standard `openapi.yaml` from the official sources, we can automatically fetch the corresponding request URLs and method names. These will be combined with local functions and sent to GPT as if invoking local features. Upon user invocation, we'll categorize and request the respective API, ensuring real-time and precise feedback.

- **Role Masking🎭**: We've integrated numerous role-based features within our local plugins. For instance, the newly added `Vue` plugin can be used to modify local Vue projects effortlessly.

- **Join the Movement🤝**: We're actively inviting passionate individuals to collaborate with us on this project! Let's move towards a "metaGPT" future and co-develop an array of fascinating role plugins.

### 🌈 Future Plans:

- **Multi-client Interactions🔗**: When running multiple clients, we aspire for these clients to exchange messages, facilitating data transfer amongst different roles.

  **Preliminary Concept💡**:

  - **Server-side⚙️**: Operated by a GPT-4 "Administrator" preset role, its main duties will encompass assigning tasks based on users' "Role Masks" and preset objectives, and subsequently evaluating task completion rates.
  
  - **Client-side🖥️**: Users can autonomously register with the server and will then be able to receive dispatched tasks and feedback on task completion rates. It can execute certain tasks autonomously and also supports interaction via a web chat interface to accomplish associated tasks.

Let's look forward to the limitless possibilities these new features can offer! 🚀🎉

- **Function Manager**: The function manager is responsible for parsing and calling the functions defined in the `functions.py` file of each plugin.

- **AI Driven**: GPT_CodeInterpreter leverages the power of AI to understand and generate human language, enabling it to handle a variety of tasks related to code interpretation.

## Current Plugins

1. **General Plugin**: This plugin provides the functionality of displaying and uploading images.

2. **Python Interpreter Plugin**: This plugin includes a Python executor for running Python code, which is very useful for tasks such as data analysis and table processing.

3. **Vue Plugin**: Currently under development, this plugin is designed to work with Vue projects, automating the entire Vue project modification through the chat interface.

## Documentation

To get started with GPT_CodeInterpreter, please refer to the following documentation:

- 📚 [How to Install and Use GPT_CodeInterpreter](docs/install.md): Learn how to install and use GPT_CodeInterpreter in your projects.

- 🚀 [Publishing GPT_CodeInterpreter on Replit](docs/replit.md): A step-by-step guide on publishing GPT_CodeInterpreter on the Replit platform.

- 📝 [Understanding Environment Variables](docs/env.md) - 🔑 Configure GPT_CodeInterpreter with essential environment variables.

## Contributing

Contributions are welcome! Please read the contribution guide to learn how to contribute to this project.

## Contact

For any inquiries or collaboration opportunities, you can reach me via email at `402087139@qq.com`. 📧

## License

This project is licensed under the terms of the MIT license. 📜

This README now includes the link to the `env.md` file, indicated with the "Understanding Environment Variables" section. It also features an emoji flag (🔑) to highlight the importance of configuring environment variables for the project. If you have any more requests or need further assistance, please let me know!

