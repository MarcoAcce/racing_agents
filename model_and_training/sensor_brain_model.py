import torch
import torch.nn as nn
import torch.nn.functional as F

class SensorBrain(nn.Module):
    def __init__(self, input_size = 14, output_size = 9, hidden_size = 32):
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.initialize_model()
    
    def initialize_model(self):
        self.fcLayer_1 = nn.Linear(
            in_features=self.input_size, 
            out_features=self.hidden_size
        )
        self.fcLayer_2 = nn.Linear(
            in_features=self.hidden_size, 
            out_features=self.hidden_size
        )
        self.outLayer = nn.Linear(
            in_features=self.hidden_size, 
            out_features=self.output_size
        )

    def forward(self, t: torch.Tensor):
        t = F.relu(self.fcLayer_1(t))
        t = F.relu(self.fcLayer_2(t))
        return self.outLayer(t)
    
    @torch.no_grad()
    def decide(self, observations)->int:
        """ Decision action for the game.  
        INPUT: 13 sensors + speed
        9 possible actions (accelerate, brake, coast) X (right, left, no_turn)
        Returns the action index
        """
        t = torch.as_tensor(observations dtype=torch.float32)
        return int(self.forward(t).argmax())
    
if __name__ == '__main__':
    #device = 'cpu'
    #if(torch.cuda.is_available()):
    #    device = 'cuda'
    #print(f"Now i'm using {device}")
    #brain = SensorBrain().to(device)
    pass