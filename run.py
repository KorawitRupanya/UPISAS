from UPISAS.strategies.ews_strategy import EwsStrategy
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
        time.sleep(5)
        strategy.get_adaptation_options()
        print('Get adaptation options...done')
        

        while True:
            # input()
            time.sleep(5)
            strategy.monitor()
            print('Monitoring done...')
            time.sleep(5)
            # there is no knowledge, if the learning is not finished, 
            #Do analyze, plan and execute
            if not strategy.knowledge.plan_data:
                start = time.time()
                if strategy.analyze(): 
                    print('Analysis done...')
                    time.sleep(5)
                    if strategy.plan():
                        print('Planning done...')
                        strategy.execute({"config" : strategy.knowledge.plan_data.get('config')})
                        print("[Execute]\tposted configuration: " + str(strategy.knowledge.plan_data.get('config')))
                        print('Execute done...')
                        end = time.time()
                print(f'Time taken to adapt: {end - start} seconds')
            # Once the learning is Finished, print the best architecture
            else:
                monitoring_data = []
                data = strategy.knowledge.monitored_fresh_data
                # Get the current config
                current_config = data["config"]
                #Find the architecture of the current config
                compostion = strategy.find_arch_info(current_config)

                monitoring_data.append({"config": current_config ,"architecture": compostion, "Response_time": strategy.response_time(strategy.knowledge.monitored_fresh_data)})
                print(f'Best architecture: {monitoring_data}')
    except:
        sys.exit(0)