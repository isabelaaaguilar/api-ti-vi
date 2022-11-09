from os import path, listdir
import tensorflow as tf
import keras

all_image_path = [path.join('images', p) for p in listdir('images') if path.isfile(path.join('images', p))]

def load_and_preprocess_image(path):
    file = tf.io.read_file(path)
    image = tf.image.decode_jpeg(file , channels=3)
    image = tf.image.resize(image, [150, 150]) # resize all images to the same size.
    image /= 255.0  # normalize to [0,1] range
    image = 2*image-1  # normalize to [-1,1] range
    return image

all_images = [load_and_preprocess_image(path) for path in all_image_path]

dict = {'3': 0, '6': 1}

# path.split('.')[0][-3:] return the name of the image ('dog' or 'cat')
labels = [path.split('.')[0][-1:] for path in all_image_path] 

all_image_labels = [dict[label] for label in labels]

#print(all_image_labels)

ds = tf.data.Dataset.from_tensor_slices((all_images, all_image_labels))

mobile_net = tf.keras.applications.MobileNetV2(input_shape=(150, 150, 3), include_top=False)
mobile_net.trainable=False # this told the model not to train the mobile_net.96, 128, 160, 192

cnn_model = keras.models.Sequential([
    mobile_net, # mobile_net is low-level layers
    keras.layers.MaxPooling2D(), 
    keras.layers.Flatten(), 
    keras.layers.Dense(64, activation="relu"), # fully-connected hidden layer 
    keras.layers.Dense(2, activation="softmax") # output layer
])

BATCH_SIZE = 32
AUTOTUNE = tf.data.experimental.AUTOTUNE

train_ds = ds.shuffle(buffer_size = len(all_image_labels))
train_ds = train_ds.repeat()
train_ds = train_ds.batch(BATCH_SIZE)
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)

cnn_model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=["accuracy"])

steps_per_epoch=tf.math.ceil(len(all_image_path)/BATCH_SIZE).numpy()
cnn_model.fit(train_ds, epochs=16, steps_per_epoch=steps_per_epoch)

cnn_model.save('classify_stars_and_galaxies.h5')
