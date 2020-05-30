from aws_cdk import (
    core,
    aws_apigateway as apigateway,
    aws_codedeploy as codedeploy,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
)

from datetime import datetime


class ApiStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_code = lambda_.Code.from_asset('./api/lambda/functions/')

        stage_options = apigateway.StageOptions(
            stage_name='v1',
            data_trace_enabled=True,
            logging_level=apigateway.MethodLoggingLevel.INFO,
            metrics_enabled=True,
            tracing_enabled=True
        )

        api = apigateway.RestApi(
            self,
            "todo-api",
            rest_api_name="ToDo Service",
            description="This service serves todo.",
            endpoint_types=[apigateway.EndpointType.REGIONAL],
            deploy_options=stage_options
        )
        tasks_resource = api.root.add_resource("tasks")
        self.add_cors_options(tasks_resource)

        # GET /tasks
        get_tasks_handler = self.generate_handler(
            "todo_get_tasks", "get_tasks.lambda_handler", self.lambda_code
        )
        self.add_method_to_resource(tasks_resource, "GET", get_tasks_handler)

        # POST /tasks
        post_tasks_handler = self.generate_handler(
            "todo_post_tasks", "post_tasks.lambda_handler", self.lambda_code
        )
        self.add_method_to_resource(tasks_resource, "POST", post_tasks_handler)

        # PUT /tasks
        update_tasks_handler = self.generate_handler(
            "todo_update_tasks", "update_tasks.lambda_handler", self.lambda_code
        )
        self.add_method_to_resource(tasks_resource, "PUT", update_tasks_handler)

        # DELETE /tasks
        delete_tasks_handler = self.generate_handler(
            "todo_delete_tasks", "delete_tasks.lambda_handler", self.lambda_code
        )
        self.add_method_to_resource(tasks_resource, "DELETE", delete_tasks_handler)

        # DynamoDB
        task_table = dynamodb.Table(
            self,
            "task_table",
            table_name="tasks_management_table",
            partition_key=dynamodb.Attribute(
                name="user_id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="task_id", type=dynamodb.AttributeType.STRING
            ),
        )

        ## Grant DynamoDB Access to Lambda functions
        task_table.grant_read_write_data(get_tasks_handler)
        task_table.grant_read_write_data(post_tasks_handler)
        task_table.grant_read_write_data(update_tasks_handler)
        task_table.grant_read_write_data(delete_tasks_handler)

        # Create CodeDeploy
        self.create_deployment_group("GetTasks", get_tasks_handler)
        self.create_deployment_group("PostTask", post_tasks_handler)
        self.create_deployment_group("UpdateTask", update_tasks_handler)
        self.create_deployment_group("DeleteTask", delete_tasks_handler)

    def generate_handler(self, function_name, handler_path, lambda_code):
        lambda_handler = lambda_.Function(
            self,
            f"{function_name}_handler",
            function_name=function_name,
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_code,
            handler=handler_path,
            tracing=lambda_.Tracing.ACTIVE,
            environment={
                "PYTHONPATH": "/var/runtime:/var/task/vendor"
            }
        )
        return lambda_handler

    def add_method_to_resource(self, apigw_resource, method, handler):
        lambda_integration = apigateway.LambdaIntegration(
            handler,
            request_templates={"application/json": '{ "statusCode": "200" }'},
            integration_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": "'*'"
                    },
                }
            ],
        )
        apigw_resource.add_method(
            method,
            lambda_integration,
            method_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": True
                    },
                }
            ],
        )

    def add_cors_options(self, apigw_resource):
        apigw_resource.add_method(
            "OPTIONS",
            apigateway.MockIntegration(
                integration_responses=[
                    {
                        "statusCode": "200",
                        "responseParameters": {
                            "method.response.header.Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                            "method.response.header.Access-Control-Allow-Origin": "'*'",
                            "method.response.header.Access-Control-Allow-Methods": "'GET,POST,PUT,DELETE,OPTIONS'",
                        },
                    }
                ],
                passthrough_behavior=apigateway.PassthroughBehavior.WHEN_NO_MATCH,
                request_templates={"application/json": '{"statusCode":200}'},
            ),
            method_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Methods": True,
                        "method.response.header.Access-Control-Allow-Origin": True,
                    },
                }
            ],
        )

    def create_deployment_group(self, group_name, handler):
        version = handler.add_version(datetime.now().isoformat())
        alias = lambda_.Alias(
            self, f'{group_name}LambdaAlias', alias_name="Dev", version=version
        )
        codedeploy.LambdaDeploymentGroup(
            self,
            f'Deploy{group_name}Lambda',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE,
        )
