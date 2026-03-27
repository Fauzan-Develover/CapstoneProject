import tensorflow as tf

def build_panic_detection_model(vocab_size=10000, max_length=100):
    inputs = tf.keras.Input(shape=(max_length,), name="input_teks")
    x = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=64, name="embedding_layer")(inputs)
    x = tf.keras.layers.GlobalAveragePooling1D(name="pooling_layer")(x)
    x = tf.keras.layers.Dense(32, activation='relu', name="dense_layer_1")(x)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid', name="output_layer")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="Panic_Detector")
    return model

if __name__ == "__main__":
    print("Membangun kerangka model")
    model = build_panic_detection_model()
    model.summary()