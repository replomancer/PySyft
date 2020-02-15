from syft._numpy.tensor.abstract import AbstractNumpyTensor


class FixedPrecisionTensor(AbstractNumpyTensor):

    def init(self, *args, **kwargs):
        self.base = 10
        self.precision_fractional = 3
        self.data = self.data * self.scaling_factor

    @property
    def scaling_factor(self):
        return self.base ** self.precision_fractional


