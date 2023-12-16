from UPISAS.strategy import Strategy
import numpy as np


class EwsStrategy(Strategy):

    def analyze(self):
        data = self.knowledge.monitored_data
        print(data)
        print("no data bala bal")
        return True;

    def plan(self):
        data = self.knowledge.analysis_data
        print(data)
        # if data > 0:
        #     # Thompson Sampling to choose the next adaptation option
        #     arm_rewards = np.random.normal(loc=data, scale=1.0, size=len(self.knowledge.adaptation_options))
        #     selected_option = np.argmax(arm_rewards)
            
        #     self.knowledge.plan_data = {"selected_option": selected_option}
        #     return True
        return True