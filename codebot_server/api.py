
from ChatGPT.ChatGPT import Chatbot 

app = FastAPI()

chatbot = None

@app.on_event("startup")
async def startup_event():
    global chatbot
    function_manager = FunctionManager(functions=[python_exec, need_install_package])
    chatbot = Chatbot(function_manager=function_manager, api_key="your_api_key", base_url="https://api.analogai.in/v1")

