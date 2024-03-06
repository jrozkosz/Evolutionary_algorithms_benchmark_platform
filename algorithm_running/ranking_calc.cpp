#include <iostream>
#include <stdexcept>
// #include "ranking_calc.h"
#include "algorithm.h"

int call_count = 0; // Global variable to store the call count

// Objective function
int objective_function(int x) {
    call_count++;
    if(call_count > 5) {
        throw std::runtime_error("Budget exhausted - limit of objective function calls reached.");
    }
    return x * x;
}

// Ranking calculation
void ranking_calc() {
    evolutionary_algorithm(objective_function);
}

int main() {
    try {
        ranking_calc();
    } catch (const std::runtime_error& e) {
        std::cout << e.what() << std::endl;
    }
    return 0;
}



























// Function decorator to count function calls
// ObjectiveFunction count_calls(ObjectiveFunction func) {
//     return [func](int x) {
//         std::cout << "Function has been called " << call_count << " times." << std::endl;
//         call_count++;
//         if (call_count > 5) {
//             throw std::runtime_error("Budget exhausted - limit of objective function calls reached.");
//         }
//         return func(x);
//     };
// }