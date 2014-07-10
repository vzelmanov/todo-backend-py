import web
import json

def main():
    urls = ["/", Hello]

    app = web.application(urls, globals())
    app.add_processor(web.loadhook(cors_headers))
    app.run()

class Hello:
    todos = []

    def GET(self):
        return json.dumps(Hello.todos)

    def POST(self):
        task = json.loads(web.data())
        task["completed"] = False
        Hello.todos.append(task)
        return json.dumps(task)

    def DELETE(self):
        Hello.todos = []
        return '[]'

    def OPTIONS(self):
        web.header("access-control-allow-methods",
                "GET,HEAD,POST,DELETE,OPTIONS,PUT")

def cors_headers():
    web.header('Access-Control-Allow-Origin', '*')
    if "HTTP_ACCESS_CONTROL_REQUEST_HEADERS" in web.ctx.env:
        web.header("access-control-allow-headers",
                web.ctx.env.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS"))

if __name__ == "__main__":
    main()
