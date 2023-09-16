import numpy as np


# Custom environment definition
class CustomEnvironment:
    def __init__(self):
        self.num_states = 5
        self.num_actions = 2
        self.transition_probabilities = np.array([
            [0.7, 0.3],
            [0.1, 0.9],
            [0.5, 0.5],
            [0.9, 0.1],
            [0.4, 0.6]
        ])
        self.rewards = np.array([10, 5, 0, 1, -5])
        self.current_state = 0  # Starting state

    def reset(self):
        self.current_state = 0  # Reset to starting state
        return self.current_state

    def step(self, action):
        next_state_probabilities = self.transition_probabilities[self.current_state]
        next_state = np.random.choice(range(self.num_states), p=next_state_probabilities)

        reward = self.rewards[next_state]
        self.current_state = next_state

        return next_state, reward


# Q-learning algorithm
def q_learning(env, learning_rate=0.1, discount_factor=0.9, num_episodes=1000):
    q_table = np.zeros((env.num_states, env.num_actions))

    for episode in range(num_episodes):
        state = env.reset()
        done = False

        while not done:
            action = np.argmax(q_table[state, :])
            next_state, reward = env.step(action)

            # Q-value update using Q-learning formula
            q_table[state, action] += learning_rate * (
                        reward + discount_factor * np.max(q_table[next_state, :]) - q_table[state, action])

            state = next_state

    return q_table


# Run Q-learning
env = CustomEnvironment()
q_table = q_learning(env)

# Print the Q-table
print("Q-table:")
print(q_table)
