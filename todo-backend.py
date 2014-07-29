import web
import json
import uuid

def main():
    urls = [
            "/", TodosCollection,
            "/(.+)", TodoItem
            ]

    app = web.application(urls, globals())
    app.add_processor(web.loadhook(cors_headers))
    app.run()

todos_globalton = {}

class TodosCollection:
    def GET(self):
        return self.todos_as_json()

    def POST(self):
        task = json.loads(web.data())

        task_uid = uuid.uuid4().hex
        task["completed"] = False
        task["url"] = web.ctx.home + "/" + task_uid

        todos_globalton[task_uid] = task

        return json.dumps(task)

    def DELETE(self):
        todos_globalton.clear()
        return self.todos_as_json()

    def OPTIONS(self):
        web.header("access-control-allow-methods",
                "GET,HEAD,POST,DELETE,OPTIONS,PUT")

    def todos_as_json(self):
        return json.dumps(todos_globalton.values())

class TodoItem:
    def GET(self, uid):
        todo = todos_globalton[uid]
        return json.dumps(todo)

    def PATCH(self,uid):
        todo = todos_globalton[uid]
        changes = json.loads(web.data())
        todo.update(changes)
        return json.dumps(todo)

    def DELETE(self,uid):
        del todos_globalton[uid]

    def OPTIONS(self,uid):
        web.header("access-control-allow-methods",
                "GET,HEAD,POST,DELETE,OPTIONS,PUT,PATCH")


def cors_headers():
    web.header('Access-Control-Allow-Origin', '*')
    if "HTTP_ACCESS_CONTROL_REQUEST_HEADERS" in web.ctx.env:
        web.header("access-control-allow-headers",
                web.ctx.env.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS"))

if __name__ == "__main__":
    main()
