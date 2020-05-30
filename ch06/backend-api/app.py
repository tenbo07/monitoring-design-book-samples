#!/usr/bin/env python3

from aws_cdk import core

from api.api_stack import ApiStack


app = core.App()
ApiStack(app, "ToDoAppBackendAPI")

app.synth()
