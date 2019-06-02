from run import app
from jinja2.exceptions import UndefinedError


@app.template_filter("catch_overall")
def add_overall(text: str):
    """Checks if the input text (event.region_name) exists, and returns Overall if it doesn't.

    Used to check if text coming from the template exists, since I can't get the region_name to say overall.
    If the region name is undefined, that means it is the overall region information, which should be titled `Overall`
    """
    try:  # Need a try/catch because a null check doesn't work here
        text.istitle()  # Just need to do some operation on the string to confirm weather or not it exists
        return text
    except UndefinedError:
        return "Overall"
