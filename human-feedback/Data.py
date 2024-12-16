import torch
from torch.utils.data import Dataset


class DistDataset(Dataset):
    def __init__(self, distribution, NodeFeatureLen, NumNodes) -> None:
        self.d = distribution
        self.n = NodeFeatureLen
        self.l = NumNodes
        self.nodeslist = []
        for node in range(NumNodes):
            self.nodeslist.append(distribution.sample(NodeFeatureLen))
        self.nodes = torch.FloatTensor(self.nodeslist)

    def __len__(self):
        return self.l

    def __getitem__(self, index):
        return self.nodes[index] 