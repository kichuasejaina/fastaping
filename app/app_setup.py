from fastapi import FastAPI

app_initiated = FastAPI(debug=True,
                        title="Sample API",
                        summary="This is a sample API Summary",
                        description="This is a sample API description",
                        version='0.1')
