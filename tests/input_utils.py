# -*- coding: utf-8 -*-
"""
This file contains method for input imagery creation for other unit tests..
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""

import numpy as np
import scipy.ndimage as image

import cellstar.utils.debug_util as debug_util


def turn_on_debug():
    debug_util.DEBUGING = True


def turn_off_debug():
    debug_util.DEBUGING = False


def prepare_image(shape):
    img = np.zeros(shape)
    img.fill(0.5)
    return img


def finish_image(img):
    img = image.gaussian_filter(img, 3)
    img = img + np.random.normal(0, 0.01, img.shape)
    return img


def draw_cell(img, center, radius):
    draw_disc(img, center, radius + 2, .8)
    draw_disc(img, center, radius, .3)


def draw_weak_cell(img, center, radius):
    draw_disc(img, center, radius + 2, .8)
    draw_disc(img, center, radius, .45)

def draw_very_weak_cell(img, center, radius):
    draw_disc(img, center, radius + 2, .55)
    draw_disc(img, center, radius, .45)


def draw_disc(img, center, radius, value):
    x, y = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    distance = np.sqrt((x - center[0]) * (x - center[0]) + (y - center[1]) * (y - center[1]))
    img[distance <= radius] = value


def get_best_mask(seg, num):
    """
    @type seg: np.ndarray
    """
    res = seg.copy()
    res[seg > num] = 0
    return res


def calculate_diff_fraction(seg, gt):
    """
    @type seg: np.ndarray
    @type gt: np.ndarray
    """
    return (float(np.count_nonzero(seg & gt))) / np.count_nonzero(seg | gt)


def calculate_diffs_per_object(seg, gt):
    """
    @type seg: np.ndarray
    @type gt: np.ndarray
    """
    ids = range(1, max(seg.max(), gt.max()) + 1)
    seg_masks = [seg == i for i in ids]
    gt_masks = [gt == i for i in ids]

    res = []
    for s in seg_masks:
        if len(gt_masks) > 0:
            diffs = [calculate_diff_fraction(s, g) for g in gt_masks]
            best_id = np.argmax(diffs)
            res.append(diffs[best_id])
            gt_masks.pop(best_id)
        else:
            res.append(0)
    return res