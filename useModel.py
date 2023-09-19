import torch as t
from myQLearningPack import DeepQNetwork
from dataGetter import getData
import numpy as np


lr = 0
nActions = 3
inputDims = [3]

model = DeepQNetwork(lr, nActions=nActions, inputDims=inputDims, fc1Dims=256, fc2Dims=256)
model.load_state_dict(t.load("savedModels/testModel.pth"))

print("Getting data...")
# trainData = getData()
print("Done!\n")

# Set the model to evaluation mode (important if using layers like Dropout)
model.eval()

# Forward pass (inference) to get predictions
with t.no_grad():
    prediction = model(t.tensor(np.array([50, 50, 50]), dtype=t.float32))
    print(t.argmax(prediction).item())
