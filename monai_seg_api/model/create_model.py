import torch
from monai.networks.nets import UNet

model = UNet(
    spatial_dims=3,  # Changed from 'dimensions' to 'spatial_dims' (MONAI convention)
    in_channels=1,
    out_channels=2,
    channels=(16, 32, 64, 128),  # Fixed to match your inference code
    strides=(2, 2, 2),  # Fixed to match your inference code
    num_res_units=2,
)

# Explicitly save to model/ directory
torch.save(model.state_dict(), "model/model.pth")