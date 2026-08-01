import os


def run(context):
    context.console.print(f"\n📁 {context.fs.pwd()}\n")