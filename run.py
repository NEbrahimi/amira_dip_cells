import os
import do_functions
reload(do_functions)

root_dir = 'C:/Users/nebr002/Desktop/53_WF/CSV/'

""" Translation Part """
fname_interpolated = '53_SBack_2_1164_dil20_edited.csv'  # nuclei detection csv file
fname_translation = 'Translation1.csv'  # matlab translation csv file from nuclei detection
do_functions.do_translation_part(os.path.join(root_dir, fname_interpolated), os.path.join(root_dir, fname_translation), cols=[9,12])


""" Eigen Part """
fname = '53_SBack_2_1164_dil20_edited_translated.csv'  # Translated full csv file
do_functions.do_eigen_part(os.path.join(root_dir, fname), cols=[12,18])
