import requests
import typer
import json
from rich.console import Console,Group
from rich.syntax import Syntax
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

app = typer.Typer()
console = Console()

layout = Layout()

layout.split_column(
    Layout(name="request"),
    Layout(name="response")
)

@app.command()
def request(
    method:str,
    url:str,
    data:str = typer.Option(None,"--data","-d",help="JSON Body"),
    header:str = typer.Option(None,"--header","-H",help="Key:Value headers"),):

    headers = {}
    if header:
        try:
            key,value = header.split(":")
            headers[key.strip()] = value.strip()
        except ValueError:
            console.print("[red]Invalid Headers! Use key:value format.[/red]")
            raise typer.Exit()
    request_content = Group(
        get_method(method),
        Text(f"URL:{url}"),
        Text(getData(data)),
        Text(getHeader(headers))
    )
    request_panel = Panel(request_content,title="Request Data")
    try:
        response = requests.request(method=method.upper(),url=url,headers=headers,data=data)

        try:
            json_obj = response.json()
            json_text = json.dumps(json_obj, indent=2)
            syntax = Syntax(json_text,"json",theme="rrt",line_numbers=True,word_wrap=False,indent_guides=True,code_width=console.width-10)
            response_content = Group(
                get_status_code(response.status_code),
                get_response_body() if syntax else "",
                syntax if syntax else ""
            )
        except Exception as e:
            response_content = Group(
                get_status_code(response.status_code),
                Text(f"{e}")
            )
    except Exception as e:
        response_content = Group(
            get_status_code(response.status_code),
            Text(f"Exception:{e}")
        )
    
    response_panel = Panel(response_content,title="Response Data")

    console.print(Panel(Group(request_panel, response_panel), title="HttpCaller"))

def get_status_code(code:int):
    status_text = Text()
    code_color = "white"
    status_text.append("Status Code : ",style="bold white")
    if(code <= 199):
        code_color = "bold blue"
    elif(code <= 299):
        code_color = "bold green"
    elif(code <= 399):
        code_color = "bold purple"
    elif(code <= 499):
        code_color = "bold yellow"
    elif(code <= 599):
        code_color = "bold red"
    else:
        code_color = "bold white"
    status_text.append(str(code),style=code_color)
    return status_text

def get_method(method:str):
    method_text_obj = Text()
    if(method):
        method_color = "white"
        method_text_obj.append("Method : ",style="bold white")
        match method:
            case "get":
                method_color = "bold green"
            case "post":
                method_color = "bold yellow"
            case "put":
                method_color = "bold orange"
            case "patch":
                method_color = "bold orange"
            case "delete":
                method_color = "bold purple"
        method_text_obj.append(f"{method.upper()}",style=f"{method_color}")
    else:
        method_text_obj.append("Undefined",style="bold red")
    return method_text_obj
    
def get_response_body():
    response_body_obj = Text()
    response_body_obj.append("Response Body: ",style="bold white")
    return response_body_obj


def getData(data):
    if data:
        return f"Data:{data}"
    else:
        return "Data: NULL"

def getHeader(headers):
    if headers:
        return f"Header:{headers}"
    else:
        return "Header: NULL"

if __name__ == "__main__":
    app()
