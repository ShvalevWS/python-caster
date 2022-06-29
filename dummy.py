from CasterClass import *

tools = Tools()

print(tools.make_line())


# def parse_headers(self, request):
#     heads = []
#     reqst_text = request.split('\r\n')
#     for elms in reqst_text:
#         if len(heads) < 4:
#             heads.append(elms)
#         else:
#             break
#     method = heads[0].split()
#     ntrip_version = heads[1]
#     user_agent = heads[2]
#     auth = heads[-1].split(':')[1][7:]
#     return auth, method[1], method[0]
