from UPISAS.strategies.ews import EwsStrategy
from UPISAS.exemplars.ews import EWS
from UPISAS.exemplars.swim import SWIM
import signal
import sys
import time


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)
if __name__ == '__main__':
    
    exemplar = EWS(auto_start=True)
    exemplar.start_run()
    time.sleep(5)
    try:
        strategy = EwsStrategy(exemplar)
        strategy.get_monitor_schema()
        strategy.get_adaptation_options_schema()
        strategy.get_execute_schema()
        

        while True:

            # input()
            time.sleep(5)
            strategy.monitor()
            print('monitor done')
            print(strategy.analyze() + "analyze done")

            if strategy.analyze(): 
                print('analyze')
                if strategy.plan():
                    strategy.execute({"config": "|../repository/TCPNetwork.o,/home/roberto/dana//components/net/TCP.o,../repository/request/RequestHandlerPT.o,../repository/app_protocols/HTTPProtocol.o,../repository/http/HTTPHeader1_0.o,../repository/http/handler/GET/HTTPGETCMP.o,/home/roberto/dana//components/io/File.o,../repository/compression/ZLIB.o,/home/roberto/dana//components/os/Run.o,/home/roberto/dana//components/time/DateUtil.o,../repository/http/util/HTTPUtil.o,/home/roberto/dana//components/data/StringUtil.o,/home/roberto/dana//components/data/adt/List.o|0:net.TCPSocket:1,0:net.TCPServerSocket:1,0:request.RequestHandler:2,2:app_protocols.AppProtocol:3,3:http.HTTPHeader:4,4:http.handler.GET.HTTPGET:5,5:io.File:6,5:compression.Compression:7,7:os.Run:8,7:time.DateUtil:9,7:io.FileSystem:6,4:http.util.HTTPUtil:10,10:io.FileSystem:6,10:data.StringUtil:11,11:data.adt.List:12|"})
    except:
        sys.exit(0)