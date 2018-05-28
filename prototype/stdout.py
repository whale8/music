import time

for i in range(0, 10):
    print(i, '\r', end='')
    time.sleep(1)

print('end')
