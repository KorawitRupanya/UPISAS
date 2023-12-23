import re
import time
from UPISAS.strategy import Strategy
import numpy as np
import random


class EwsStrategy(Strategy):

    def analyze(self):
        analysis_data = []
        data = self.knowledge.monitored_fresh_data
        # Get the current config
        current_config = data["config"]
        print(f'Current config: {current_config}')

        compostion = self.find_arch_info(current_config)
        print(f'Current architecture: {compostion}')

        analysis_data.append({"config": current_config ,"architecture": compostion, "Response_time": self.response_time(self.knowledge.monitored_fresh_data)})
        print(f'Analysis data1: {analysis_data}')

        #print(f'Current architecture: {compostion}')
        list_of_config = self.knowledge.adaptation_options['configs']
        
        for config in list_of_config:
            #print(f'Config: {config}')
            time.sleep(3)
            self.execute({"config": config})
            time.sleep(2)
            self.monitor()
            compostion = self.find_arch_info(config)
            #print(f'Current architecture: {compostion}')
            analysis_data.append({"config": config ,"architecture": compostion, "Response_time": self.response_time(self.knowledge.monitored_fresh_data)})
            #print(f'Analysis data1: {analysis_data}')

        self.knowledge.analysis_data = analysis_data
        print(f'Analysis data2: {self.knowledge.analysis_data}')
        
        return True;

    def plan(self):
        start = time.time()
        # Example config list
        data = self.knowledge.analysis_data
        exploration_time_frame = 10
        upper_confidence_bound_parameter = 2

        # Call ucb_algorithm
        best_config = self.ucb_algorithm(data, exploration_time_frame, upper_confidence_bound_parameter)
        #best_config = self.epsilon_greedy(data, 0.1)
        print(f'Best architecture: {best_config}')
        end = time.time()
        print(f'Time taken to find the Best architecture for UCB algo: {(end - start)*1000} ms')
        # Set the plan data to the best config found
        self.knowledge.plan_data = best_config

        return True

    def response_time(self, data):
        # Initialize counter and value with default values
        counter = None
        value = None
        # Get the Response time from the monitored data and clients
        for metric in data['metrics']:
            if metric['name'] == 'response_time':
                counter = metric['counter']
                value = metric['value']
                break

        # Print the counter and value
        if counter is not None and value is not None:
            response_time = value / counter
            print(f'"Response_time: {response_time} ms."')
            return response_time
        else:
            print('No metric found with name "response_time"')
        return None

    def find_arch_info(self, input_string):
        # Extracting the substrings using regular expressions
        request_handler_match = re.search(r"\.\./repository/request/(\w+\.o)", input_string)
        httpgetchcmp_match = re.search(r"\.\./repository/http/handler/GET/(\w+\.o)", input_string)
        gz_match = re.search(r"\.\./repository/compression/(\w+\.o)", input_string)
        cache_handler_lru_match = re.search(r"\.\./repository/cache/(\w+\.o)", input_string)

        # Creating the output list
        output_list = []

        # Adding items to the output list if matches are found
        if request_handler_match:
            output_list.append(request_handler_match.group(1))

        if httpgetchcmp_match:
            output_list.append(httpgetchcmp_match.group(1))

        if gz_match:
            output_list.append(gz_match.group(1))

        if cache_handler_lru_match:
            output_list.append(cache_handler_lru_match.group(1))

        return output_list
    

    def ucb_algorithm(self, config_list, exploration_time_frame, upper_confidence_bound_parameter):
    # Initialize variables
        average_rewards = np.zeros(len(config_list))
        trial_counts = np.zeros(len(config_list))

        # Exploration phase
        for _ in range(exploration_time_frame):
            # Select a random config
            random_config_index = random.randint(0, len(config_list) - 1)

            # Calculate the reward for the selected config
            reward = self.reward_function(config_list[random_config_index])

            # Update average reward and trial count
            average_rewards[random_config_index] = (average_rewards[random_config_index] * trial_counts[random_config_index] + reward) / (trial_counts[random_config_index] + 1)
            trial_counts[random_config_index] += 1

        # Exploitation phase
        for _ in range(exploration_time_frame, len(config_list)):
            # Calculate upper confidence bounds for all configs
            upper_confidence_bounds = average_rewards + upper_confidence_bound_parameter * np.sqrt(np.log(len(config_list)) / trial_counts)

            # Select the config with the highest upper confidence bound
            best_config_index = np.argmax(upper_confidence_bounds)

            # Calculate the reward for the selected config
            reward = self.reward_function(config_list[best_config_index])

            # Update average reward and trial count
            average_rewards[best_config_index] = (average_rewards[best_config_index] * trial_counts[best_config_index] + reward) / (trial_counts[best_config_index] + 1)
            trial_counts[best_config_index] += 1

        # Return the config with the highest average reward
        best_config_index = np.argmax(average_rewards)
        return config_list[best_config_index]
    

    def epsilon_greedy(self,config_list, exploration_rate):
        # Sort the data by response time in ascending order
        sorted_data = sorted(config_list, key=lambda x: x['Response_time'])

        # Choose the best configuration with probability 1 - epsilon
        if random.random() > exploration_rate:
            return sorted_data[0]
        else:
            # Choose a random configuration with probability epsilon
            return random.choice(config_list)

    def reward_function(self, config):
        # Calculate the reward for the given config
        response_time = config.get("Response_time")
        if response_time is not None and response_time > 0:
            reward = 1000 / response_time
            return reward
        else:
            return 1
