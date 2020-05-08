def hello(environ, start_response):
    query_string = environ['QUERY_STRING']
    data = ""
    if query_string != "":
        param_lst = query_string.split('&')
        for param in param_lst:
            name_value = param.split('=')
            data += f"{name_value[0]}={name_value[1]}\n"
    data = data.encode("utf-8")

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])
