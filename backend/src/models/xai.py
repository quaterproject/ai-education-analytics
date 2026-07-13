import os
import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def get_last_conv_layer_name(model):
    for layer in reversed(model.layers):
        if isinstance(layer, (tf.keras.layers.Conv2D, tf.keras.layers.Conv1D)):
            return layer.name
    raise ValueError("No convolutional layer found in model.")

def generate_gradcam(model_path, img_path, output_path, class_idx=None):
    """
    Generates Grad-CAM heatmap for a CNN model and superimposes it on the input image.
    """
    # Load model and image
    model = tf.keras.models.load_model(model_path)
    
    img = Image.open(img_path).resize((64, 64))
    img_array = np.array(img).astype(np.float32) / 255.0
    
    # Add batch dimension
    img_tensor = np.expand_dims(img_array, axis=0)
    
    # If no class specified, choose the predicted class
    preds = model(img_tensor).numpy()
    if class_idx is None:
        class_idx = np.argmax(preds[0])
        
    last_conv_layer_name = get_last_conv_layer_name(model)
    
    # Compute gradients manually tracing layer inputs
    img_tensor_tf = tf.convert_to_tensor(img_tensor)
    with tf.GradientTape() as tape:
        tape.watch(img_tensor_tf)
        x = img_tensor_tf
        conv_outputs = None
        for layer in model.layers:
            x = layer(x)
            if layer.name == last_conv_layer_name:
                conv_outputs = x
        predictions = x
        loss = predictions[:, class_idx]
        
    grads = tape.gradient(loss, conv_outputs)
    
    # Mean intensity of gradient for each channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Weigh the feature map channels
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Relu on heatmap
    heatmap = tf.maximum(heatmap, 0.0)
    
    # Normalize between 0 and 1
    max_val = tf.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val
        
    heatmap = heatmap.numpy()
    
    # Resize heatmap to original image size
    heatmap_img = Image.fromarray(np.uint8(255 * heatmap))
    heatmap_img = heatmap_img.resize((img.size[0], img.size[1]), Image.Resampling.BILINEAR)
    heatmap_arr = np.array(heatmap_img) / 255.0
    
    # Use matplotlib jet colormap
    from matplotlib import colormaps
    colormap = colormaps['jet']
    colormap_colors = colormap(heatmap_arr)[:, :, :3]
    
    # Superimpose heatmap on original image
    superimposed = colormap_colors * 0.45 + img_array * 0.55
    superimposed = np.clip(superimposed, 0.0, 1.0)
    
    # Save superimposed image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    res_img = Image.fromarray(np.uint8(255 * superimposed))
    res_img.save(output_path)
    
    return float(preds[0][class_idx]), int(class_idx)


def generate_perturbation_importance(model_path, csv_path):
    """
    Computes perturbation importance for tabular time-series features.
    Features: [temperature, vibration, pressure]
    """
    model = tf.keras.models.load_model(model_path)
    
    # Load input data (10 timesteps, 3 features)
    data = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    if len(data.shape) == 1:
        data = data.reshape(10, 3)
        
    # Baseline prediction
    baseline_tensor = np.expand_dims(data, axis=0)  # Shape (1, 10, 3)
    baseline_preds = model.predict(baseline_tensor)[0]
    predicted_class = np.argmax(baseline_preds)
    baseline_score = baseline_preds[predicted_class]
    
    feature_names = ["temperature", "vibration", "pressure"]
    importances = []
    
    # Perturb each feature and observe change in predicted class probability
    for f_idx in range(3):
        perturbed_data = data.copy()
        # Perturb by adding zero noise or zeroing it out, or shifting it
        # Let's zero it out (or shift by 0.5) to see the drop
        perturbed_data[:, f_idx] = 0.0
        
        perturbed_tensor = np.expand_dims(perturbed_data, axis=0)
        perturbed_preds = model.predict(perturbed_tensor)[0]
        
        # Change in predicted class probability
        drop = max(0.0, baseline_score - perturbed_preds[predicted_class])
        importances.append(drop)
        
    # Normalize to sum to 1
    total = sum(importances)
    if total > 0:
        importances = [imp / total for imp in importances]
    else:
        # Default fallback equal weights if no impact
        importances = [0.33, 0.33, 0.33]
        
    importance_dict = {name: float(importance) for name, importance in zip(feature_names, importances)}
    
    return importance_dict, int(predicted_class), [float(v) for v in baseline_preds]
