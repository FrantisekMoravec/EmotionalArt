import datetime

import torch
import os
import numpy as np
from PIL import Image
import legacy
import dnnlib


# Loading pretrained model
def load_model(model_path):
    with dnnlib.util.open_url(model_path) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to('cuda')
    return G


# Generating random image
def generate_image(G, z):
    label = torch.zeros([1, G.c_dim], device='cuda')  # Bez labelu
    img = G(z, label, truncation_psi=0.5, noise_mode='const')
    img = (img * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    img = img.permute(0, 2, 3, 1)
    return img[0].cpu().numpy()


def save_image(image_array, directory, image_name):
    image = Image.fromarray(image_array)
    if not os.path.exists(directory):
        os.makedirs(directory)
    image_path = os.path.join(directory, image_name)
    image.save(image_path)
    return image_path


# Initialising model (now I'm using model for cat images)
def initialize_and_generate_image(model_path='pretrained_models/afhqcat.pkl'):
    G = load_model(model_path)
    z = torch.from_numpy(np.random.randn(1, G.z_dim)).to('cuda')
    generated_image = generate_image(G, z)
    return generated_image


def create_run_directory(base_directory='runs'):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    run_directory = os.path.join(base_directory, current_time)
    if not os.path.exists(run_directory):
        os.makedirs(run_directory)
    return run_directory
