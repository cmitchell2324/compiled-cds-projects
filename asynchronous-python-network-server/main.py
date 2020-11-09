from aiohttp import web
import os
import random
import string
import logging
import asyncio


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    f = open(name, "r")
    return web.Response(text= f.read())


async def apprun(host = 'localhost', port = 8080):
    log = logging.Logger("%a %r %T")
    app = web.Application(logger=log)
    app.add_routes([web.get('/', handle),
                       web.get("/{name}", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    print(f"Hosting app on localhost:8080")
    return runner, site


if __name__ == '__main__':
    for i in range(50):
        open('file%s.txt' % i, 'r').close()

    dirname = os.path.dirname(__file__)
    for filename in os.listdir(dirname):
        chars = ''.join([random.choice(string.ascii_letters) for i in range(10000)])
        if filename.endswith(".txt"):
            filename = open(filename, 'w').write(chars)
        else:
            continue

    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    task = loop.create_task(apprun())
    runner, site = loop.run_until_complete(task)
    loop.run_forever()
