'''
# References
    - [A Neural Algorithm of Artistic Style](http://arxiv.org/abs/1508.06576)
    - https://github.com/keras-team/keras/blob/master/examples/neural_style_transfer.py
'''

from __future__ import print_function
from keras.preprocessing.image import load_img, save_img, img_to_array
import numpy as np
from scipy.optimize import fmin_l_bfgs_b
from keras.applications import vgg19
from keras import backend as K

class Styler():
    def __init__(self, iter=1, tv_w=1.0, c_w=1.0, s_w=0.025):
        self.iterations=iter
        self.total_variation_weight = tv_w
        self.style_weight = s_w
        self.content_weight = c_w
        self.model = None

    def change_style(self, base_img, style_img, result_path):
        width, height = load_img(base_img).size
        img_nrows = 400
        img_ncols = int(width * img_nrows / height)

        # get tensor representations of our images
        base_image = K.variable(preprocess_image(base_img, img_nrows, img_ncols))
        style_reference_image = K.variable(preprocess_image(style_img,img_nrows, img_ncols))

        # this will contain our generated image
        if K.image_data_format() == 'channels_first':
            combination_image = K.placeholder((1, 3, img_nrows, img_ncols))
        else:
            combination_image = K.placeholder((1, img_nrows, img_ncols, 3))

        # combine the 3 images into a single Keras tensor
        input_tensor = K.concatenate([base_image,
                                      style_reference_image,
                                      combination_image], axis=0)
        if self.model is None: #TODO check that the input_tensor is the right size
            # build the VGG19 network with our 3 images as input
            # the model will be loaded with pre-trained ImageNet weights
            self.model = vgg19.VGG19(input_tensor=input_tensor,
                                weights='imagenet', include_top=False)

        # get the symbolic outputs of each "key" layer (we gave them unique names).
        outputs_dict = dict([(layer.name, layer.output) for layer in self.model.layers])
        # combine these loss functions into a single scalar
        loss = K.variable(0.0)
        layer_features = outputs_dict['block5_conv2']
        base_image_features = layer_features[0, :, :, :]
        combination_features = layer_features[2, :, :, :]
        loss += self.content_weight * content_loss(base_image_features,
                                              combination_features)

        feature_layers = ['block1_conv1', 'block2_conv1',
                          'block3_conv1', 'block4_conv1',
                          'block5_conv1']

        for layer_name in feature_layers:
            layer_features = outputs_dict[layer_name]
            style_reference_features = layer_features[1, :, :, :]
            combination_features = layer_features[2, :, :, :]
            sl = style_loss(style_reference_features, combination_features, img_nrows, img_ncols)
            loss += (self.style_weight / len(feature_layers)) * sl
        loss += self.total_variation_weight * total_variation_loss(combination_image, img_nrows, img_ncols)

        # get the gradients of the generated image wrt the loss
        grads = K.gradients(loss, combination_image)

        outputs = [loss]
        if isinstance(grads, (list, tuple)):
            outputs += grads
        else:
            outputs.append(grads)

        f_outputs = K.function([combination_image], outputs)

        evaluator = Evaluator(f_outputs, img_nrows, img_ncols)

        # run scipy-based optimization (L-BFGS) over the pixels of the generated image
        # so as to minimize the neural style loss
        x = preprocess_image(base_img, img_nrows, img_ncols)

        for i in range(self.iterations):
            x, min_val, info = fmin_l_bfgs_b(evaluator.loss, x.flatten(),
                                             fprime=evaluator.grads, maxfun=20)
            print(i)

        #save_img(result_path, deprocess_image(x, img_nrows, img_ncols))

        return deprocess_image(x, img_nrows, img_ncols)

# util function to open, resize and format pictures into appropriate tensors
def preprocess_image(image_path, img_nrows, img_ncols):
    img = load_img(image_path, target_size=(img_nrows, img_ncols))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return img

# util function to convert a tensor into a valid image
def deprocess_image(x, img_nrows, img_ncols):
    if K.image_data_format() == 'channels_first':
        x = x.reshape((3, img_nrows, img_ncols))
        x = x.transpose((1, 2, 0))
    else:
        x = x.reshape((img_nrows, img_ncols, 3))
    # Remove zero-center by mean pixel
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    # 'BGR'->'RGB'
    x = x[:, :, ::-1]
    x = np.clip(x, 0, 255).astype('uint8')
    return x

# the gram matrix of an image tensor (feature-wise outer product)
def gram_matrix(x):
    assert K.ndim(x) == 3
    if K.image_data_format() == 'channels_first':
        features = K.batch_flatten(x)
    else:
        features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram

# the "style loss" is designed to maintain the style of the reference image in the generated image.
def style_loss(style, combination, img_nrows, img_ncols):
    assert K.ndim(style) == 3
    assert K.ndim(combination) == 3
    S = gram_matrix(style)
    C = gram_matrix(combination)
    channels = 3
    size = img_nrows * img_ncols
    return K.sum(K.square(S - C)) / (4.0 * (channels ** 2) * (size ** 2))

# an auxiliary loss function designed to maintain the "content" of the base image in the generated image
def content_loss(base, combination):
    return K.sum(K.square(combination - base))

# the 3rd loss function, total variation loss, designed to keep the generated image locally coherent
def total_variation_loss(x, img_nrows, img_ncols):
    assert K.ndim(x) == 4
    if K.image_data_format() == 'channels_first':
        a = K.square(
            x[:, :, :img_nrows - 1, :img_ncols - 1] - x[:, :, 1:, :img_ncols - 1])
        b = K.square(
            x[:, :, :img_nrows - 1, :img_ncols - 1] - x[:, :, :img_nrows - 1, 1:])
    else:
        a = K.square(
            x[:, :img_nrows - 1, :img_ncols - 1, :] - x[:, 1:, :img_ncols - 1, :])
        b = K.square(
            x[:, :img_nrows - 1, :img_ncols - 1, :] - x[:, :img_nrows - 1, 1:, :])
    return K.sum(K.pow(a + b, 1.25))

def eval_loss_and_grads(x, f_outputs, img_nrows, img_ncols):
    if K.image_data_format() == 'channels_first':
        x = x.reshape((1, 3, img_nrows, img_ncols))
    else:
        x = x.reshape((1, img_nrows, img_ncols, 3))
    outs = f_outputs([x])
    loss_value = outs[0]
    if len(outs[1:]) == 1:
        grad_values = outs[1].flatten().astype('float64')
    else:
        grad_values = np.array(outs[1:]).flatten().astype('float64')
    return loss_value, grad_values

# this Evaluator class makes it possible to compute loss and gradients in one pass
# while retrieving them via two separate functions, "loss" and "grads".
class Evaluator(object):

    def __init__(self, f_outputs, img_nrows, img_ncols):
        self.loss_value = None
        self.grads_values = None
        self.f_outputs = f_outputs
        self.img_nrows = img_nrows
        self.img_ncols = img_ncols

    def loss(self, x):
        assert self.loss_value is None
        loss_value, grad_values = eval_loss_and_grads(x, self.f_outputs, self.img_nrows, self.img_ncols)
        self.loss_value = loss_value
        self.grad_values = grad_values
        return self.loss_value

    def grads(self, x):
        assert self.loss_value is not None
        grad_values = np.copy(self.grad_values)
        self.loss_value = None
        self.grad_values = None
        return grad_values

