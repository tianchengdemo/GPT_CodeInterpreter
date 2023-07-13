# GPT_CodeInterpreter

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python (3.8+ recommended).
- You have installed Chainlit.

## Installing Chainlit

To install Chainlit, follow these steps:

```bash
pip install chainlit
```

## Environment Variables

Before running the project, you need to set up the following environment variables. You can set these in your shell, or add them to a `.env` file in the root directory of the project.

Replace `<your_value>` with your actual values.

```bash
export OPENAI_API_KEY=<your_value>
export OPENAI_API_BASE=<your_value>
export SD_API_KEY=<your_value>
export MYSQL_USER=<your_value>
export MYSQL_PASSWORD=<your_value>
export MYSQL_HOST=<your_value>
export MYSQL_DATABASE=<your_value>
```

## Running the Project with Environment Variables

If you're setting up the environment variables in a `.env` file, you'll need to use a Python package like `python-dotenv` to load the variables when you run your script.

To install `python-dotenv`, run:

```bash
pip install python-dotenv
```

Then, in your `main.py` script, you'll need to load the environment variables at the beginning of your script:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Using GPT_CodeInterpreter

To use GPT_CodeInterpreter, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/boyueluzhipeng/GPT_CodeInterpreter.git
```

2. Navigate to the project directory:

```bash
cd GPT_CodeInterpreter
```

3. Run the main script:

```bash
python main.py
```

## Contact

If you want to contact me you can reach me at 402087139@qq.com