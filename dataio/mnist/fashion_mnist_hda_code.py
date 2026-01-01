import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from PIL import Image


device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
    )
    def forward(self,x):
        x = self.flatten(x)
        logits = self.linear_relu(x)
        return logits


def run_prediction():
    model_path = hou.pwd().parm('model').eval()    
    
    model = Net().to(device)
    model.load_state_dict(torch.load(model_path, weights_only=True))
    model.eval()
    
    image_path = hou.pwd().parm('img').eval()
    image = Image.open(image_path).convert("L")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((28,28))
    ])
    
    image = transform(image).to(device)
    
    with torch.inference_mode():
        output = model(image)
        prediction = torch.argmax(output).item()
    return prediction  
    
def class_lookup(prediction):
        clothing_items = {
                "0": "tshirt",
                "1": "trouser",
                "2": "pullover",
                "3": "dress",
                "4": "coat",
                "5": "sandal",
                "6": "shirt",
                "7": "sneaker",
                "8": "bag",
                "9": "ankle boot"
        }
        output = clothing_items.get(prediction)
        return output    
        
def main():
    prediction = run_prediction()
    answer = class_lookup(str(prediction))
    hou.pwd().parm('answer_out').set(answer) 


    
