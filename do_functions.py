import utils
reload(utils)
import numpy as np


def do_translation_part(filename1, filename2, option='translation', header=True, cols=None):

    """ Get centroids """
    if cols is None:
        centroid_interpolated = utils.get_data(filename1,
                                               cols=cols)
    else:
        centroid_interpolated = utils.get_data(filename1,
                                               cols=[cols[0], cols[1]])  # change cols if cx,cy,cz columns change
    centroid_translation = utils.get_data(filename2)

    """ Get interpolation """
    xy_interpolated = utils.intepolate(centroid_interpolated, centroid_translation)

    """ Translate back """
    centroid_translated_back = utils.translate(centroid_interpolated, xy_interpolated)

    """ Save translation file """
    if cols is None:
        utils.save_file(filename1, centroid_translated_back, option=option, header=header,
                        cols=cols)
    else:
        utils.save_file(filename1, centroid_translated_back, option=option, header=header,
                        cols=[cols[0], cols[1]])  # change cols if cx,cy,cz columns change

    return None


def do_eigen_part(filename, option='eigen', header=True, cols=None):

    if cols is None:
        s_values = utils.get_data(filename, delim=',', header=header, cols=cols)
    else:
        s_values = utils.get_data(filename, delim=',', header=header, cols=[cols[0], cols[1]])

    cov_M = np.zeros((s_values.shape[0], 3, 3))
    s_M = np.zeros((s_values.shape[0], 3))
    v_M = np.zeros((s_values.shape[0], 3, 3))

    values = np.zeros((s_values.shape[0], 12))
    for i in range(len(cov_M)):
        cov_M[i] = utils.make_covariance(s_values[i])
        _, s_M[i], v_M[i] = utils.svd(cov_M[i])

        values[i, 0:9] = v_M[i].reshape(9)
        values[i, 9:] = s_M[i]

    utils.save_file(filename, values, option=option, header=header, cols=None)

    return None
