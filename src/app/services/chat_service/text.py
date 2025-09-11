import torch
print("CUDA available?", torch.cuda.is_available())
print("Device:", torch.cuda.current_device() if torch.cuda.is_available() else "CPU")