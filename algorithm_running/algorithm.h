#ifndef EVOLUTIONARY_ALGORITHM_H
#define EVOLUTIONARY_ALGORITHM_H

#include <iostream>

void evolutionary_algorithm(int (*obj_function)(int)) {
    std::cout << "User code executed" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << obj_function(5) << std::endl;
        std::cout << "ObjFunction called" << std::endl;
    }
}

#endif // EVOLUTIONARY_ALGORITHM_H
