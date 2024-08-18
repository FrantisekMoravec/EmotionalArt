# EmotionalArt

EmotionalArt is a project that combines emotion recognition through a camera with the generation of artworks using StyleGAN2-ADA. The project's goal is to create an artwork that adapts to the user's current emotions and can be further modified according to those emotions or based on text input.

## Project Features

- **Emotion Recognition:** The user's emotions are captured in real-time using a camera.
- **Image Generation:** A random image is generated based on a pre-trained StyleGAN2-ADA model.

## Requirements

Before running the project, make sure you have installed:
- NVIDIA graphics card in your computer
- [CUDA toolkit](developer.nvidia.com/cuda-downloads)
- The libraries listed in `requirements.txt`
- Downloaded pre-trained StyleGAN2-ADA models

## Usage

1. **Running the Project:**

    ```bash
    python path/to/project/EmotionalArt/stylegan2_ada_pytorch/main.py
    ```

2. **Interacting with the UI:**

    - **Emotion Display:** Emotion detection happens in real-time, with emotions displayed in a column at the bottom of the UI.
    - **Image Generation:** Click the "Generate Random Image" button to generate a new image using StyleGAN2-ADA.

## Installation of Pre-Trained Models

**To run the program, you need to install the following models and move them to the corresponding directories:**

- stylegan2-ada-pytorch/pretrained_models/[afhqcat.pkl](https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/)

## Future Plans

- Optimization of model loading and usage performance.
- Expanding support for more emotions and image adjustments.
- Adding the option to select custom models and configurations.
- Adding a text input in the UI for image adjustments using CLIP.
- Outpainting: The generated image will be automatically expanded using Stable Diffusion.
- Image adjustment based on emotions using CLIP.
