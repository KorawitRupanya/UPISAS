from UPISAS.strategy import Strategy


class EmptyStrategy(Strategy):

    def analyze(self):
        return True

    def plan(self):
        return True

    def getInfoArchitecture(arch):
        request = getRequest(arch)
        defGet = getGET(arch)
        cmp = getCMP(arch)
        ch = getCH(arch)
        result = []
        if request is not None:
            result.append(request)
        if defGet is not None:
            result.append(defGet)
        if cmp is not None:
            result.append(cmp)
        if ch is not None:
            result.append(ch)
        return result

    def getRequest(arch):
        compsList = arch.split(',')
        for comp in compsList:
            if comp.startswith('..repository/request/'):
                return comp.split('/')[-1]
        return None

    def getGET(arch):
        compsList = arch.split(',')
        for comp in compsList:
            if comp.startswith('..repository/http/handler/GET/'):
                return comp.split('/')[-1]
        return None

    def getCMP(arch):
        compsList = arch.split(',')
        for comp in compsList:
            if comp.startswith('..repository/compression/'):
                return comp.split('/')[-1]
        return None

    def getCH(arch):
        compsList = arch.split(',')
        for comp in compsList:
            if comp.startswith('..repository/cache/'):
                return comp.split('/')[-1]
        return None
