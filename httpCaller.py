import requests
import typer
import json
from rich.console import Console,Group
from rich.syntax import Syntax
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.console import RenderableType

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
    json_payload = None
    request_items: list[RenderableType] = [
        get_method(method),
        get_url_header(url)
    ]
    json_payload_header = None
    if header:
        try:
            json_payload_header = json.loads(header)
            request_items.append(get_header_header())
            request_items.append(get_header_body(json_payload_header))
        except ValueError:
            console.print("[red]Invalid Headers! Use key:value format.[/red]")
            raise typer.Exit()
    if data:
        try:
            json_payload = json.loads(data)
            request_items.append(get_data_body())
            request_items.append(get_data_obj(data))
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON Input![/red]")
            json_payload = None
    else:
        json_payload = None
    request_content = Group(*request_items)
    request_panel = Panel(request_content,title="Request Data")
    try:
        response = requests.request(method=method.upper(),url=url,headers=json_payload_header,json=json_payload)

        try:
            json_obj = response.json()
            json_text = json.dumps(json_obj, indent=2)
            syntax = Syntax(json_text,"json",theme="rrt",line_numbers=True,word_wrap=False,indent_guides=True,code_width=console.width-10)
            response_content = Group(
                get_status_code(response.status_code),
                get_response_body() if syntax else Text(""),
                syntax
            )
        except json.JSONDecodeError:
            response_content = Group(
                get_status_code(response.status_code),
                get_response_body(),
                Text(response.text)
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


def get_data_body():
    request_data_obj = Text()
    request_data_obj.append("Request Body: ",style="bold white")
    return request_data_obj

def get_data_obj(data:str):
    if not data:
        return Text("")
    try:
        json_obj = json.loads(data)
        json_text = json.dumps(json_obj,indent=2)
        syntax = Syntax(json_text,"json",theme="rrt",line_numbers=True,word_wrap=False,indent_guides=True,code_width=console.width-10)
        return syntax
    except Exception:
        console.print("Invalid JSON Input!",style="bold red")
        return Text("")

def get_url_header(url:str):
    response_data_obj = Text()
    response_data_obj.append("URL: ",style="bold white")
    if url:
        response_data_obj.append(f"{url}",style="bold yellow underline")
    return response_data_obj

def get_header_body(json_payload_header):
    json_text = json.dumps(json_payload_header, indent=2)
    syntax = Syntax(json_text,"json",theme="rrt",line_numbers=True,word_wrap=False,indent_guides=True,code_width=console.width-10)
    return syntax

def get_header_header():
    return Text("Headers: ",style="bold white")

if __name__ == "__main__":
    app()
