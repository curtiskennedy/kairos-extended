import torch
from torch.utils.data import Dataset


class DistDataset(Dataset):
    def __init__(self, distribution, NodeFeatureLen, NumNodes) -> None:
        self.d = distribution
        self.n = NodeFeatureLen
        self.l = NumNodes
        self.nodes = []
        for node in range(NumNodes):
            self.nodes.append(distribution.sample(NodeFeatureLen))
        self.nodes = torch.FloatTensor(self.nodes)

    def __len__(self):
        return self.l

    def __getitem__(self, index):
        return self.nodes[index] 