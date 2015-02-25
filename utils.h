#ifndef _utils_h_
#define _utils_h_

#include <stdio.h>
#include <stdlib.h>

#include <string>
using namespace std;

#define CHECK(cond) if (!(cond)) {fprintf(stderr, "OUCH %s:%d\n", __FILE__, __LINE__); abort(); }

#ifdef __GNUC__
/**
 * Tell the compiler to do printf format string checking if the
 * compiler supports it.
 */
#define PRINTF_ATTRIBUTE(arg1,arg2) \
  __attribute__((__format__ (__printf__, arg1, arg2)))

/**
 * Tell the compiler to do scanf format string checking if the
 * compiler supports it.
 */
#define SCANF_ATTRIBUTE(arg1,arg2) \
    __attribute__((__format__ (__scanf__, arg1, arg2)))

#else // __GNUC__

#define PRINTF_ATTRIBUTE(arg1, arg2)
#define SCANF_ATTRIBUTE(arg1, arg2)

#endif // else __GNUC__

#endif
