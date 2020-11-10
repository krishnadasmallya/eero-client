from abc import abstractproperty


class Session(object):
    @abstractproperty
    def cookie(self):
        pass
