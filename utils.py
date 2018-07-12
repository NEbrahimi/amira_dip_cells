import numpy as np


def get_data(filename, delim=',', header=True, cols=None):
    import csv

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=delim, quotechar='|')

        if header:
            reader.next()

        data = []
        for row in reader:
            if cols is None:
                data.append(row[:])
            else:
                data.append(row[cols[0]:cols[1]])

    return np.asarray(data).astype(np.float64)


def intepolate(c1, c2):
    """
    1D linear interpolation from numpy.interp

    :param c1: coordinates of inteporlated data
    :param c2: coordinates of interest
    :return:
    """

    z_translation = c2[:,2]
    y_translation = c2[:,1]
    x_translation = c2[:,0]

    z_interpolated = c1[:,2]

    x_interp = np.interp(z_interpolated, z_translation, x_translation)
    y_interp = np.interp(z_interpolated, z_translation, y_translation)

    return np.array(zip(x_interp, y_interp))


def translate(c1, xy_interp):
    c1_new = c1.copy()
    c1_new[:,0:2] = c1_new[:,0:2] - xy_interp

    return c1_new


def save_file(filename_original, values, option='translation', header=True, cols=None):
    import csv
    eigenrow = ['EVector1x','EVector1y','EVector1z','EVector2x','EVector2y','EVector2z',
                'EVector3x','EVector3y','EVector3z','EValue1','EValue2','EValue3']

    if option == 'translation':
        new_file = filename_original.replace('.csv', '_translated.csv')
    elif option == 'eigen':
        new_file = filename_original.replace('.csv', '_eigen.csv')

    with open(filename_original, 'r') as f:
        print("Saving the new file. Please wait...")
        reader = csv.reader(f, delimiter=',', quotechar='|')

        with open(new_file, 'w') as w:
            writer = csv.writer(w, delimiter=',', quotechar='|', lineterminator='\n')

            if option == 'eigen':
                header_row = []
                temp_header = reader.next()
                for i in range(len(temp_header)):
                    header_row.append(temp_header[i])
                header_row.extend(eigenrow)
                writer.writerow(header_row)
            elif option == 'translation':
                writer.writerow(reader.next())
            else:
                raise Exception("Incorrect header option!")


        with open(new_file, 'a') as a:
            writer = csv.writer(a, delimiter=',', quotechar='|', lineterminator='\n')

            count = 0

            for row in reader:
                if cols is None and option == 'translation':
                    new_row = []
                    new_row.append(values[:,0][count])
                    new_row.append(values[:,1][count])
                    new_row.append(values[:,2][count])
                    writer.writerow(new_row)
                elif cols is not None and option == 'translation':
                    new_row = []
                    new_row.extend(row[0:cols[0]])
                    new_row.append(values[:,0][count])
                    new_row.append(values[:,1][count])
                    new_row.append(values[:,2][count])
                    new_row.extend(row[cols[1]:])
                    writer.writerow(new_row)
                elif cols is None and option == 'eigen':
                    new_row = []
                    new_row.extend(row)
                    new_row.append(values[:,0][count])
                    new_row.append(values[:,1][count])
                    new_row.append(values[:,2][count])
                    new_row.append(values[:,3][count])
                    new_row.append(values[:,4][count])
                    new_row.append(values[:,5][count])
                    new_row.append(values[:,6][count])
                    new_row.append(values[:,7][count])
                    new_row.append(values[:,8][count])
                    new_row.append(values[:,9][count])
                    new_row.append(values[:,10][count])
                    new_row.append(values[:,11][count])
                    writer.writerow(new_row)
                else:
                    raise Exception("Incorrect Options or Cols!")

                count+=1

        print("count is %i" %count)
        f.close()
        w.close()
        print("File saved in %s " %(new_file))
    return None


def make_covariance(data):
    """
    Constructs a covariance matrix using S values

    :param data: np array of shape 1x6
    :return:
    """

    return np.array(
        [
            [data[0], data[1], data[2]],
            [data[1], data[3], data[4]],
            [data[2], data[4], data[5]]
        ]
    )


def svd(M):
    """
    Performs singular value decomposition on a 3x3 covariance matrix

    :param M: np array of shape 3x3
    :return:
    """

    U, s, V = np.linalg.svd(M)

    return U, s, V