# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from func import linear
from rnns import cell as cell


class olrn(cell.Cell):
    """The Recurrence-Free Addition-Subtraction Twin-Gated Recurrent Unit.
    Or, output-gated lightweight recurrent network
    """

    def __init__(self, d, ln=False, scope='olrn'):
        super(olrn, self).__init__(d, ln=ln, scope=scope)

    def get_init_state(self, shape=None, x=None, scope=None):
        return self._get_init_state(
            self.d, shape=shape, x=x, scope=scope)

    def fetch_states(self, x):
        with tf.variable_scope(
                "fetch_state_{}".format(self.scope or "olrn")):
            h = linear(x, self.d * 4,
                       bias=False, ln=self.ln, scope="hide_x")
        return (h, )

    def __call__(self, h_, x):
        # h_: the previous hidden state
        # p,q,r,s/x: the current input state
        """
            p, q, r, s = W x
            i = sigmoid(p + h_)
            f = sigmoid(q - h_)
            h = i * r + f * h_
            o = simoid(s - h)
            h = o * h
        """
        if isinstance(x, (list, tuple)):
            x = x[0]

        with tf.variable_scope(
                "cell_{}".format(self.scope or "atr")):
            p, q, r, s = tf.split(x, 4, -1)

            i = tf.sigmoid(p + h_)
            f = tf.sigmoid(q - h_)

            h = i * r + f * h_

            o = tf.nn.sigmoid(s - h)
            h = o * h

        return h
