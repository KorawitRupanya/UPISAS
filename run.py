from UPISAS.strategies.ews import EwsStrategy
from UPISAS.exemplars.ews import EWS
from UPISAS.exemplars.swim import SWIM
import sys
import time

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
            print('monitoring done...')
            time.sleep(5)
            strategy.get_adaptation_options()
            print('get_adaptation_options done')
            time.sleep(5)
            if strategy.analyze(): 
                print('analysis done...')
                time.sleep(5)
                if strategy.plan():
                    print('plan done...')
                    strategy.execute({"config" : strategy.knowledge.plan_data})
                    print('execute done...')
    except:
        sys.exit(0)