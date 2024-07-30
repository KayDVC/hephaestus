#ifndef ARRAYLIST_H
#define ARRAYLIST_H

#include <cstdint>
#include <vector>
#include "hephaestus/common/sizes.hpp"
#include "hephaestus/common/math.hpp"


/************************************************************
 * @brief A wrapper for the std::vector class that prevents
 * fully dynamic memory allocation. Developers must explicitly 
 * increase size of buffer.
 ************************************************************/
namespace Hephaestus {
namespace Containers {

    template <typename T> class ArrayList {

        using reference = T&;

        constexpr uint32_t defaultSize = 8*KILOBYTE;

        private:
            uint32_t idx = 0;
            uint32_t capacity = 0;
            std::vector<T> buffer;

        public:

            // Constructors
            ArrayList(const uint32_t& size){
                capacity = size;
                buffer.reserve(size);
            };

            ArrayList() : ArrayList{defaultSize};

            // Destructor
            ~ArrayList() = default;

            /******************************************************************
             * @brief   Returns the current number of items in the internal 
             *          buffer.
             *****************************************************************/
            const uint32_t length() {
                return idx;
            }

            /******************************************************************
             * @brief   Returns the total current maximum size of the internal 
             *          buffer.
             *****************************************************************/
            const uint32_t capacity() {
                return capacity;
            }

            const reference operator[](int _idx){
                return buffer[idx];
            }

            bool pushback(const T&&){
                
            }

        
    };
}
}

#endif