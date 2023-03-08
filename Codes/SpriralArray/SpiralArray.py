import itertools
import sys

def spiral_array(w, h):
	array = [-1]*w*h
	turn_points = itertools.chain(*zip(range(w,-1,-1), range(h-1,-1,-1)))
	point = turn_points.next()
	v = 1+0j
	x = y = 0
	for i in range(w*h):
		array[y*w + x] = i
		point -= 1	
		if point < 1:
			v *= 1j
			point = turn_points.next()
		x += int(v.real)
		y += int(v.imag)
	return array

w, h = int(sys.argv[1]), int(sys.argv[2])
result = spiral_array(w,h)
char_count = len(str(w*h))
f = (("%"+str(char_count+2)+"d") * w +"\n") * h
print(f % tuple(result))