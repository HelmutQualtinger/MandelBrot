#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

// Function to calculate the Mandelbrot set
int mandelbrot(double real, double imag, int max_iter)
{
    double z_real = real;
    double z_imag = imag;
    int iter = 0;

    while (iter < max_iter)
    {
        double z_real_squared = z_real * z_real;
        double z_imag_squared = z_imag * z_imag;

        if (z_real_squared + z_imag_squared > 4.0)
        {
            break;
        }

        double new_real = z_real_squared - z_imag_squared + real;
        double new_imag = 2.0 * z_real * z_imag + imag;

        z_real = new_real;
        z_imag = new_imag;

        iter++;
    }

    return iter;
}

int main()
{
    // Image dimensions
    int width = 4000;
    int height = 2500;

    // Mandelbrot parameters
    double min_real = -2.0;
    double max_real = 1.0;
    double min_imag = -1.5;
    double max_imag = 1.5;
    int max_iter = 1000;

    // Open a pipe to sips command
    FILE *pipe = popen("sips -s format jpeg -o mandelbrot1.jpg", "w");
    if (!pipe)
    {
        std::cerr << "Error opening pipe to sips command" << std::endl;
        return 1;
    }

    // Write PPM header to the pipe
    fprintf(pipe, "P6\n%d %d\n255\n", width, height);

    // Calculate and write Mandelbrot set to the pipe
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            double real = min_real + (max_real - min_real) * x / (width - 1);
            double imag = min_imag + (max_imag - min_imag) * y / (height - 1);

            int iter = mandelbrot(real, imag, max_iter);

            // Convert iteration count to RGB color
            unsigned char r = (iter % 8) * 32;
            unsigned char g = (iter % 16) * 16;
            unsigned char b = (iter % 32) * 8;

            // Write color to the pipe
            fprintf(pipe, "%c%c%c", r, g, b);
        }
    }

    // Close the pipe
    pclose(pipe);

    return 0;
}
