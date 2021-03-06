"""Activation functions.
Reference:
https://github.com/keras-team/keras/blob/master/keras/activations.py
https://en.wikipedia.org/wiki/Activation_function
"""
import numpy as np


class Sigmoid():
    """Sigmoid activation function."""

    def __call__(self, x):
        return 1. / (1. + np.exp(-x))

    def gradient(self, x):
        return self.__call__(x) * (1 - self.__call__(x))


class Softmax():
    def __call__(self, x, axis=-1):
        """Softmax activation function.
        # Arguments
            x: Input tensor.
            axis: Integer, axis along which the softmax normalization is applied.
        # Returns
            Tensor, output of softmax transformation.
        # Raises
            ValueError: In case `dim(x) == 1`.
        """
        ndim = np.ndim(x)
        if ndim == 2:
            y = np.exp(x - np.max(x, axis, keepdims=True))
            return y / np.sum(y, axis, keepdims=True)
        elif ndim > 2:
            e = np.exp(x - np.max(x, axis=axis, keepdims=True))
            s = np.sum(e, axis=axis, keepdims=True)
            return e / s
        else:
            raise ValueError('Cannot apply softmax to a tensor that is 1D. '
                             'Received input: %s' % x)

    def gradient(self, x):
        p = self.__call__(x)
        return p * (1 - p)


class TanH():
    """Hyperbolic tangent activation function.

    The hyperbolic activation:
        `tanh(x) = (exp(x) - exp(-x)) / (exp(x) + exp(-x))`
    """

    def __call__(self, x):
        return 2 / (1 + np.exp(-2 * x)) - 1

    def gradient(self, x):
        return 1 - np.power(self.__call__(x), 2)


class ReLU():
    """Rectified Linear Unit.
    
    With default values, it returns element-wise `max(x, 0)`.
    Otherwise, it follows:
    `f(x) = max_value` for `x >= max_value`,
    `f(x) = x` for `threshold <= x < max_value`,
    `f(x) = alpha * (x - threshold)` otherwise.
    """

    def __call__(self, x):
        return np.where(x >= 0, x, 0)

    def gradient(self, x):
        return np.where(x >= 0, 1, 0)


class LeakyReLU():
    def __init__(self, alpha=0.1):
        self.alpha = alpha

    def __call__(self, x):
        return np.where(x >= 0, x, self.alpha * x)

    def gradient(self, x):
        return np.where(x >= 0, 1, self.alpha)


class ELU():
    def __init__(self, alpha=0.1):
        self.alpha = alpha

    def __call__(self, x):
        return np.where(x >= 0.0, x, self.alpha * (np.exp(x) - 1))

    def gradient(self, x):
        return np.where(x >= 0.0, 1, self.__call__(x) + self.alpha)


class SELU():
    """
    https://arxiv.org/abs/1706.02515
    https://github.com/bioinf-jku/SNNs/blob/master/SelfNormalizingNetworks_MLP_MNIST.ipynb
    """

    def __init__(self):
        self.scale = 1.0507009873554804934193349852946
        self.alpha = 1.6732632423543772848170429916717

    def __call__(self, x):
        return self.scale * np.where(x >= 0.0, x, self.alpha * (np.exp(x) - 1))

    def gradient(self, x):
        return self.scale * np.where(x >= 0.0, 1, self.alpha * np.exp(x))


class SoftPlus():
    def __call__(self, x):
        return np.log(1 + np.exp(x))

    def gradient(self, x):
        return 1 / (1 + np.exp(-x))
