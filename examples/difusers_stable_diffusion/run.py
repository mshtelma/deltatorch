# Databricks notebook source
!/databricks/python3/bin/python -m pip install diffusers==0.16.1 accelerate>=0.18.0 torch==2.0.0 torchvision datasets  xformers tensorboard git+https://github.com/mshtelma/deltatorch ftfy tensorboard Jinja2

# COMMAND ----------

!/databricks/python3/bin/python -m pip install  git+https://github.com/huggingface/diffusers.git


# COMMAND ----------

!cd ../../ && /databricks/python3/bin/python -m pip install  -U .

# COMMAND ----------

# MAGIC %pip install accelerate>=0.18.0

# COMMAND ----------

!accelerate launch --mixed_precision fp16 --multi_gpu  --num_processes 8 train_text_to_image_lora.py \
--pretrained_model_name_or_path="CompVis/stable-diffusion-v1-4" \
--train_data_dir="/dbfs/tmp/msh/lambdalabs_pokemon_blip_captions.delta" \
--resolution=512 \
--random_flip \
--train_batch_size=5 \
--num_train_epochs=100 \
--checkpointing_steps=1000 \
--learning_rate=1e-04 --lr_scheduler="constant" \
--lr_warmup_steps=0 \
--seed=42 \
--output_dir="/dbfs/msh/deltatorch/diffusers/sd-pokemon-model-lora-v3" \
--report_to="tensorboard" \
--validation_prompt="cute dragon creature"

# COMMAND ----------

from diffusers import StableDiffusionPipeline
import torch

model_path = "/dbfs/msh/deltatorch/diffusers/sd-pokemon-model-lora-v3/"

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16
)
pipe.unet.load_attn_procs(model_path)
pipe.to("cuda")

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt, num_inference_steps=45, guidance_scale=7.5).images[0]
image

# COMMAND ----------

pipe("a photo of an astronaut riding a horse on mars", num_inference_steps=50, guidance_scale=7.5).images[0]

# COMMAND ----------

pipe("Dinasour on the Moon", num_inference_steps=50, guidance_scale=7.5).images[0]

# COMMAND ----------

pipe("Dinasours and pokemons", num_inference_steps=50, guidance_scale=7.5).images[0]

# COMMAND ----------

pipe("Dinasours in central park", num_inference_steps=50, guidance_scale=7.5).images[0]

# COMMAND ----------


