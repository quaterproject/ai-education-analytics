import os
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw

# Create necessary directories
os.makedirs("data/models", exist_ok=True)
os.makedirs("data/samples", exist_ok=True)

print("TensorFlow Version:", tf.__version__)

# ---------------------------------------------------------
# 1. Train LSTM Model (Tabular / Time Series)
# ---------------------------------------------------------
print("\n--- Training LSTM Model ---")
# Shape: (samples, time_steps=10, features=3)
# Features: [temperature_anomaly, vibration_level, pressure_drop]
num_samples = 500
X_lstm = np.random.rand(num_samples, 10, 3).astype(np.float32)
y_lstm = np.zeros(num_samples, dtype=np.int32)

# Set some logic: if average vibration (feature 1) > 0.6 and average temperature (feature 0) > 0.5 -> High Risk (2)
# if average vibration > 0.4 -> Medium Risk (1) else Low Risk (0)
for i in range(num_samples):
    avg_temp = np.mean(X_lstm[i, :, 0])
    avg_vib = np.mean(X_lstm[i, :, 1])
    if avg_vib > 0.6 and avg_temp > 0.5:
        y_lstm[i] = 2  # High Risk
    elif avg_vib > 0.4:
        y_lstm[i] = 1  # Medium Risk
    else:
        y_lstm[i] = 0  # Low Risk

model_lstm = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(10, 3)),
    tf.keras.layers.LSTM(16),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model_lstm.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model_lstm.fit(X_lstm, y_lstm, epochs=5, batch_size=32, verbose=1)
# model_lstm.save("data/models/lstm_risk_model.h5")
model_lstm.save("data/models/lstm_risk_model.keras")
print("Saved LSTM model to data/models/lstm_risk_model.keras")

# ---------------------------------------------------------
# 2. Train CNN Model (Image Classification)
# ---------------------------------------------------------
print("\n--- Training CNN Model ---")
# 64x64 RGB images
# Class 0: Healthy (uniform gray background with subtle noise)
# Class 1: Damaged (uniform gray background with dark lines/scratches)
num_images = 400
X_cnn = []
y_cnn = []

for i in range(num_images):
    # Create background
    img = Image.new("RGB", (64, 64), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    
    # Label
    label = np.random.choice([0, 1])
    if label == 1:
        # Draw "cracks/scratches"
        for _ in range(np.random.randint(2, 6)):
            x1, y1 = np.random.randint(5, 59, size=2)
            x2, y2 = np.random.randint(5, 59, size=2)
            draw.line([(x1, y1), (x2, y2)], fill=(20, 20, 20), width=np.random.randint(1, 3))
    
    # Add minor noise
    img_arr = np.array(img).astype(np.float32) / 255.0
    img_arr += np.random.normal(0, 0.02, img_arr.shape)
    img_arr = np.clip(img_arr, 0.0, 1.0)
    
    X_cnn.append(img_arr)
    y_cnn.append(label)

X_cnn = np.array(X_cnn).astype(np.float32)
y_cnn = np.array(y_cnn).astype(np.int32)

model_cnn = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(64, 64, 3)),
    tf.keras.layers.Conv2D(8, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model_cnn.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model_cnn.fit(X_cnn, y_cnn, epochs=5, batch_size=32, verbose=1)
model_cnn.save("data/models/cnn_damage_model.keras")

print("Saved CNN model to data/models/cnn_damage_model.keras")

# ---------------------------------------------------------
# 3. Train ANN Model (Audio Classification)
# ---------------------------------------------------------
print("\n--- Training ANN Model ---")
# 1D audio feature vectors (13 features, representing MFCCs)
# Class 0: Normal machinery sound
# Class 1: Anomalous machinery sound
num_audio = 500
X_ann = np.random.rand(num_audio, 13).astype(np.float32)
y_ann = np.zeros(num_audio, dtype=np.int32)

# Logic: If features 0, 4, 8 sum to > 1.8, then Anomalous (1)
for i in range(num_audio):
    if X_ann[i, 0] + X_ann[i, 4] + X_ann[i, 8] > 1.8:
        y_ann[i] = 1
    else:
        y_ann[i] = 0

model_ann = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(13,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model_ann.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model_ann.fit(X_ann, y_ann, epochs=5, batch_size=32, verbose=1)
model_ann.save("data/models/ann_audio_model.keras")
print("Saved ANN model to data/models/ann_audio_model.keras")

# ---------------------------------------------------------
# 4. Generate Test Samples for CLI / Web App Demo
# ---------------------------------------------------------
print("\n--- Generating Test Samples ---")
# Save sample tabular CSV: columns = sensor1, sensor2, sensor3 (representing 10 timesteps)
sample_tabular = np.random.rand(10, 3) * 0.8
# Force some anomalies so the model evaluates it as medium or high risk
sample_tabular[:, 0] = sample_tabular[:, 0] + 0.2  # high temp
sample_tabular[:, 1] = sample_tabular[:, 1] + 0.3  # high vib
np.savetxt("data/samples/sample_sensor_data.csv", sample_tabular, delimiter=",", header="temperature,vibration,pressure", comments="")
print("Saved data/samples/sample_sensor_data.csv")

# Save a healthy image and a damaged image
img_healthy = Image.new("RGB", (64, 64), color=(200, 200, 200))
img_healthy.save("data/samples/sample_healthy.png")

img_damaged = Image.new("RGB", (64, 64), color=(200, 200, 200))
draw_d = ImageDraw.Draw(img_damaged)
draw_d.line([(10, 10), (50, 50)], fill=(20, 20, 20), width=3)
draw_d.line([(50, 10), (10, 50)], fill=(20, 20, 20), width=2)
img_damaged.save("data/samples/sample_damaged.png")
print("Saved sample images to data/samples/")

# Save sample audio feature vector (CSV)
sample_audio_normal = np.random.rand(13) * 0.4
sample_audio_anomaly = np.random.rand(13) * 0.4
sample_audio_anomaly[[0, 4, 8]] = [0.8, 0.7, 0.9]  # anomaly
np.savetxt("data/samples/sample_audio_features.csv", [sample_audio_normal, sample_audio_anomaly], delimiter=",", header=",".join([f"mfcc_{i}" for i in range(13)]), comments="")
print("Saved data/samples/sample_audio_features.csv")

print("\nModel training and generation complete!")
