import requests

from sm import settings


class SaltAPI:
    def __init__(self, url=settings.SALT_SERVER_URL, username=settings.SALT_SERVER_USER,
                 password=settings.SALT_SERVER_PASSWORD):
        if url[-1] == '/':
            self.__url = url[:-1]
        else:
            self.__url = url
        self.__username = username
        self.__password = password
        self.__session = self.login()

    def login(self):
        url = self.__url + "/login"
        json = {
            'username': self.__username,
            'password': self.__password,
            'eauth': 'pam',
        }
        session = requests.Session()
        session.post(url, json=json)
        return session

    def minions(self, mid=''):
        url = self.__url + "/minions"
        if mid and mid != '*':
            url += "/" + mid
        rsp = self.__session.get(url)
        return rsp.json()

    def cmd(self, client, fun, targetType, target, arg=None, kwarg=None):
        if arg is None:
            arg = []
        if kwarg is None:
            kwarg = {}
        json = [{
            'client': client,
            'fun': fun,
            'expr_form': targetType,
            'tgt': target,
            'arg': arg,
            'kwarg': kwarg,
        }]
        rsp = self.__session.post(self.__url, json=json)
        return rsp.json()

    def jobs(self, jid=''):
        if jid:
            url = self.__url + "/jobs/" + jid
        else:
            url = self.__url + "/jobs"
        rsp = self.__session.get(url)
        return rsp.json()

    def run(self, client, fun, arg=None, kwarg=None):
        if arg is None:
            arg = []
        if kwarg is None:
            kwarg = {}
        json = [{
            'client': client,
            'fun': fun,
            'arg': arg,
            'kwarg': kwarg,
        }]
        rsp = self.__session.post(self.__url, json=json)
        return rsp.json()

    def writeFile(self, path, data):
        json = [{
            'client': 'wheel',
            'fun': 'file_roots.write',
            'path': path,
            'data': data,
        }]
        rsp = self.__session.post(self.__url, json=json)
        return rsp.json()

    def deleteFile(self, path):
        # TODO：目前没有相关接口，先把文件内容置空
        return self.writeFile(path, '# wait to delete')

    def readPillar(self, path):
        json = [{
            'client': 'wheel',
            'fun': 'pillar_roots.read',
            'path': path,
        }]
        rsp = self.__session.post(self.__url, json=json)
        return rsp.json()['return'][0]['data']['return'][0][settings.PILLAR_ROOT + path]

    def writePillar(self, path, data):
        json = [{
            'client': 'wheel',
            'fun': 'pillar_roots.write',
            'path': path,
            'data': data,
        }]
        rsp = self.__session.post(self.__url, json=json)
        return rsp.json()

    def deletePillar(self, path):
        # TODO：目前没有相关接口，先把文件内容置空
        return self.writePillar(path, "# wait to delete")


if __name__ == '__main__':
    api = SaltAPI()
    # json = api.cmd(client='local', fun='state.sls', target='local_Center', targetType='list', arg=['sm.test', ],
    #                kwarg={'pillar': {'service_group': 'group', 'service_type': 'type'}, })
    # print(json['return'][0])
    rsp = api.jobs("20170307111049032127")
    data = rsp['info'][0]['Result']
    print(data)
