import logging;logging.basicConfig(level = logging.INFO)

import asyncio
import aiomysql

@asyncio.coroutine
def create_poll(loop,**kw):
    logging.info('create databse connnection poll....')
    global __poll
    __poll = yield from aiomysql.create_poll(
        host = kw.get('host','localhost'),
        port = kw.get('port',3306),
        user = kw['user'],
        password = kw['password'],
        db=kw['db'],
        charset = kw.get('charset','utf-8'),
        autocommit = kw.get('autocommit',True),
        maxsize = kw.get('maxsize',10),
        minsize = kw.get('minsize',1),
        loop = loop
    )
    
@asyncio.coroutine
def select(sql,args,size = None):
    logging.info(args,size)
    global __poll
    with (yield from __poll) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execue(sql.replace('?','%s'),args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned:%s' % len(rs))
        return rs



loop = asyncio.get_event_loop()
create_poll(loop)
rs = select('select * from file','')
for r in rs:
    print(r)


