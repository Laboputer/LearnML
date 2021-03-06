'''
This code is based on
https://github.com/hunkim/DeepRL-Agents
'''
import gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

env = gym.make('FrozenLake-v0')

# Input and output size based on the Env
input_size = env.observation_space.n
output_size = env.action_space.n
learning_rate = 0.1

# Set Q-learning related parameters
dis = .99
num_episodes = 2000

# Create lists to contain total rewards and steps per episode
rList = []
def one_hot(x):
    return np.identity(16)[x:x + 1]

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(units=output_size, input_dim=input_size))
model.compile(loss='mse', optimizer=tf.keras.optimizers.SGD(lr=learning_rate))

print("Learing Started....")
for i in range(num_episodes):
    if i % 100 == 0:
        print("steps : ", i)
    
    # Reset environment and get first new observation
    s = env.reset()
    e = 1. / ((i / 50) + 10)
    rAll = 0
    done = False
    local_loss = []

    # The Q-Network training
    while not done:
        # Choose an action by greedily (with e chance of random action)
        # from the Q-network

        Qs = model.predict(one_hot(s))
        if np.random.rand(1) < e:
            a = env.action_space.sample()
        else:
            a = np.argmax(Qs)

        # Get new state and reward from environment
        s1, reward, done, _ = env.step(a)
        if done:
            # Update Q, and no Qs+1, since it's a terminal state
            Qs[0, a] = reward
        else:
            # Obtain the Q_s1 values by feeding the new state through our
            # network
            Qs1 = model.predict(one_hot(s1))
            # Update Q
            Qs[0, a] = reward + dis * np.max(Qs1)

        # Train our network using target (Y) and predicted Q (Qpred) values
        model.fit(one_hot(s), Qs, epochs=1, verbose=0)
        rAll += reward
        s = s1
    rList.append(rAll)
          
print("Percent of successful episodes: " +
      str(sum(rList) / num_episodes) + "%")
plt.bar(range(len(rList)), rList, color="blue")
plt.show()