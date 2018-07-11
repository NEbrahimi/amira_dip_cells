import numpy as np
import os

root_dir = 'C:/Users/nebr002/Desktop/53_WF/CSV/'


def get_centroid(filename, delim=',', header=True, cols=None):
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


def save_file(filename_original, translated_values, header=True, cols=None):
    import csv

    new_file = filename_original.replace('.csv', '_translated.csv')

    with open(filename_original, 'r') as f:
        print("Saving the new file. Please wait...")
        reader = csv.reader(f, delimiter=',', quotechar='|')

        with open(new_file, 'w') as w:
            writer = csv.writer(w, delimiter=',', quotechar='|', lineterminator='\n')

            if header:
                writer.writerow(reader.next())

        with open(new_file, 'a') as a:
            writer = csv.writer(a, delimiter=',', quotechar='|', lineterminator='\n')

            count = 0
            for row in reader:
                if cols is None:
                    writer.writerow(row)
                else:
                    new_row = row[0:cols[0]]
                    new_row.append(translated_values[:,0][count])
                    new_row.append(translated_values[:,1][count])
                    new_row.append(translated_values[:,2][count])
                    new_row.extend(row[cols[1]:])

                    writer.writerow(new_row)
                    count+=1

        print("count is %i" %count)
        f.close()
        w.close()
        print("File saved in %s " %(new_file))
    return None


""" Define file names """
fname_interpolated = '53_SBack_2_1164_dil20_edited.csv'  # nuclei detection csv file
fname_translation = 'Translation1.csv'  # matlab translation csv file from nuclei detection

""" Get centroids """
centroid_interpolated = get_centroid(os.path.join(root_dir, fname_interpolated), cols=[9,12])  # change cols if cx,cy,cz columns change
centroid_translation = get_centroid(os.path.join(root_dir, fname_translation))

""" Get interpolation """
xy_interpolated = intepolate(centroid_interpolated, centroid_translation)

""" Translate back """
centroid_translated_back = translate(centroid_interpolated, xy_interpolated)

""""""
save_file(os.path.join(root_dir, fname_interpolated), centroid_translated_back, header=True, cols=[9,12])   # change cols if cx,cy,cz columns change