from fastapi import APIRouter, Request, Response

response_router = APIRouter(prefix="/debug")


@response_router.get('/headers')
def get_headers(req: Request, resp: Response):
    resp.headers.append('test', 'testy')
    return {
        'req_headers': req.headers,
        'resp_headers': resp.headers
    }

# @response_router.put('/headers')
# def get_headers(req: Request, resp: Response):
#     resp.headers.append('test', 'testy')
#     return {
#         'req_headers': req.headers,
#         'resp_headers': resp.headers
#     }