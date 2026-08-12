import json


class ToolExecutor:
    def __init__(self, fs):
        self.fs = fs

    def execute(self, tool_call):
        tool = json.loads(tool_call)

        tool_name = tool.get("tool")
        args = tool.get("args", {})

        match tool_name:

            case "read_file":
                return self.fs.read_file(
                    args["path"]
                )

            case "write_file":
                self.fs.write_file(
                    args["path"],
                    args["content"],
                )

                return f"Created {args['path']}"

            case "edit_file":
                self.fs.edit_file(
                    args["path"],
                    args["old_text"],
                    args["new_text"],
                )

                return f"Edited {args['path']}"

            case "run_command":
                return self.fs.run_command(
                    args["command"]
                )

            case _:
                return f"Unknown tool: {tool_name}"