## static link
# Compile library files
gcc -c lib_mylib.c -o lib_mylib.o

# Create static library.
ar rcs lib_mylib.a lib_mylib.o

# compile the main program
gcc -c driver.c -o driver.o

# link the compiled driver program to the static library
gcc -o driver driver.o -L. -l_mylib

# Run the driver program
./driver

## dynamic link
# -shared instructs the compiler that we are building a shared library
# -fPIC is to generate position independent code.
gcc -shared -fPIC -o liblibrary.so library.c

# compile and link
gcc application.c -L./ -llibrary -o sample
