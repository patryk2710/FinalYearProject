# class machine for holding jwt and detector model
class Machine:
    def __init__(self, JWT):
        self._JWT = JWT

    def get_JWT(self):
        return self._JWT
