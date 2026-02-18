import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
import logging
import os
from .config import Config
from .models import ModelFactory

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Trainer for the AI models."""
    
    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def prepare_data(self, df: pd.DataFrame, target_col: str = 'close'):
        """Prepare sequences for LSTM training."""
        data = df.filter([target_col]).values
        # Simple normalization
        self.mean = data.mean()
        self.std = data.std()
        normalized_data = (data - self.mean) / self.std
        
        X, y = [], []
        seq_length = 60 # Look back 60 candles
        for i in range(len(normalized_data) - seq_length):
            X.append(normalized_data[i:i+seq_length])
            y.append(normalized_data[i+seq_length])
            
        return torch.FloatTensor(np.array(X)), torch.FloatTensor(np.array(y))

    def train_lstm(self, df: pd.DataFrame):
        """Train the LSTM model."""
        X, y = self.prepare_data(df)
        dataset = TensorDataset(X, y)
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        model = ModelFactory.get_model('lstm', input_dim=1).to(self.device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        model.train()
        for epoch in range(10): # Example epochs
            total_loss = 0
            for batch_X, batch_y in loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            logger.info(f"Epoch {epoch+1}, Loss: {total_loss/len(loader)}")
            
        return model

    def save_model(self, model, path: str):
        """Save the model state."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(model.state_dict(), path)
        logger.info(f"Model saved to {path}")
