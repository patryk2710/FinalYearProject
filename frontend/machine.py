# class machine for holding jwt and detector model
class Machine:
    def __init__(self, JWT, dnn_net, layerNames):
        self._JWT = JWT
        self._dnn_net = dnn_net
        self._layerNames = layerNames

    def get_JWT(self):
        return self._JWT

    def get_net(self):
        return self._dnn_net

    def get_layerNames(self):
        return self._layerNames