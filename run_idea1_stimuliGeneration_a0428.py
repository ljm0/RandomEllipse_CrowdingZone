# method 1
import os
import time

i_loop=30101

start = time.time()
while(i_loop <= 30150):
    #run serial
    # os.system('python idea1_crowding_virtual_ellipses_psycopy_adjusted_scale.py' + ' ' + str(i_loop))
    # #run parallel /b /min
    os.system('start /min python idea1_crowding_virtual_ellipses_psycopy_adjusted_scale.py' + ' ' + str(i_loop))
    time.sleep(0.01)
    print(i_loop)
    i_loop += 1
end = time.time()

print('time', str(end-start))
# import virtual_ellipses_underPython
# virtual_ellipses_underPython.main()
