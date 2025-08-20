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
        Text(f"Method:{method}"),
        Text(f"URL:{url}"),
        Text(getData(data)),
        Text(getHeader(headers))
    )
    layout["request"].update(Panel(request_content,title="Request Data"))
    try:
        response = requests.request(method=method.upper(),url=url,headers=headers,data=data)

        try:
            json_obj = response.json()
            json_text = json.dumps(json_obj, indent=2)
            syntax = Syntax(json_text,"json",theme="monokai",line_numbers=True)
            response_content = Group(
                Text(f"Status Code:{response.status_code}"),
                syntax
            )
            layout["response"].update(Panel(response_content,title="Response Data"))
        except Exception:
            response_content = Group(
                Text(f"Status Code:{response.status_code}"),
                Text(f"Resonse Message:{response.text}")
            )
            layout["response"].update(Panel(response_content,title="Response Data"))
    except Exception as e:
        response_content = Group(
            Text(f"Exception:{e}")
        )
        layout["response"].update(Panel(response_content,title="Response Data"))
    console.print(Panel(layout, title="HttpCaller"))

def getData(data):
    if data:
        return f"Data:{data}"
    else:
        return "NULL"

def getHeader(headers):
    if headers:
        return f"Header:{headers}"
    else:
        return "NULL"

if __name__ == "__main__":
    app()
