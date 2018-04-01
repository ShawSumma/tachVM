# tachVM
functional tachyon

tachyon is a functional language that uses python standard library
it is not purely functional, because of python interop
here is a taste
```
//this is tachyon

fac(x) = fac(x-1)*x
fac(0) = 1
curry_me_add(x,y) = x+y
next = curry_me_add(1)
print(next(10))
```
