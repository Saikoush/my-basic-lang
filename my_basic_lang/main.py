# my_basic_lang/main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from my_basic_lang.lexer import Lexer
from my_basic_lang.parser import Parser
from my_basic_lang.interpreter import Interpreter

app = FastAPI()

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="my_basic_lang/static"), name="static")

# Set template directory
templates = Jinja2Templates(directory="my_basic_lang/templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "code": "", "output": ""})

@app.post("/run", response_class=HTMLResponse)
async def run_code(request: Request, code: str = Form(...)):
    try:
        # Step 1: Lexical Analysis
        lexer = Lexer(code)
        tokens = lexer.generate_tokens()

        # Step 2: Parsing
        parser = Parser(tokens)
        ast = parser.parse()

        # Step 3: Interpretation
        interpreter = Interpreter()
        output = interpreter.interpret(ast)

    except Exception as e:
        output = f"Error: {str(e)}"

    return templates.TemplateResponse("index.html", {"request": request, "code": code, "output": output})
