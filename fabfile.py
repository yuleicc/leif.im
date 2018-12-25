from fabric import Connection


def deploy():
    c = Connection('yuleicc@leif.yuleicc')
    result = c.run('uname -s')


def hello():
    print('hello')
