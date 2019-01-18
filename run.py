# method 1
import os
i_loop=1

if os.path.exists('info.csv'):
    os.remove('info.csv')

while(i_loop <= 3):
    os.system('python virtual_ellipses_psycopy_adjusted_scale.py' + ' ' + str(i_loop))
    i_loop += 1

# import virtual_ellipses_underPython
# virtual_ellipses_underPython.main()
