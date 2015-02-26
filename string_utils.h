/*
  Copyright 2008 Google Inc.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

#ifndef _STRING_UTILS_H__
#define _STRING_UTILS_H__

#include <cstring>
#include <cstdarg>
#include <map>
#include <string>
#include <vector>
#include <stdint.h>         // Integer types and macros.

#include "utils.h"


struct CharPtrComparator {
  bool operator()(const char* s1, const char* s2) const {
    return strcmp(s1, s2) < 0;
  }
};


struct CaseInsensitiveCharPtrComparator {
  bool operator()(const char* s1, const char* s2) const {
    return strcasecmp(s1, s2) < 0;
  }
};

struct CaseInsensitiveStringComparator {
  bool operator()(const std::string &s1, const std::string &s2) const {
    return strcasecmp(s1.c_str(), s2.c_str()) < 0;
  }
};

typedef std::vector<std::string> StringVector;



/**
 * Removes the starting and ending spaces from a string.
 */
std::string TrimString(const std::string &s);

/**
 * Converts a string into lowercase.
 * Note: Only converts ASCII chars.
 */
std::string ToLower(const std::string &s);

/**
 * Converts a string into uppercase.
 * Note: Only converts ASCII chars.
 */
std::string ToUpper(const std::string &s);

/**
 * Format data into a C++ string.
 */
std::string StringPrintf(const char *format, ...)
  // Tell the compiler to do printf format string checking.
  PRINTF_ATTRIBUTE(1,2);
std::string StringVPrintf(const char *format, va_list ap);

/**
 * Append result to a supplied string
 */
void StringAppendPrintf(std::string *dst, const char *format, ...)
  PRINTF_ATTRIBUTE(2,3);
void StringAppendVPrintf(std::string *dst, const char *format, va_list ap);

/**
 * URI-encode the source string.
 * Note: don't encode a valid uri twice, which will give wrong result.
 */
std::string EncodeURL(const std::string &source);

/**
 * URI-encode the source string as a URI component.
 * Note: don't encode a valid uri twice, which will give wrong result.
 */
std::string EncodeURLComponent(const std::string &source);

/** URI-decode the source string. */
std::string DecodeURL(const std::string &source);

/** Returns whether the given character is valid in a URI. See RFC2396. */
bool IsValidURLChar(char c);
bool IsValidURLComponentChar(char c);

/** Returns the scheme of a url, eg. http, https, etc. */
std::string GetURLScheme(const char *url);

/**
 * Returns whether the given url scheme is valid or not.
 *
 * Valid url schemes are:
 * http, https, feed, file, mailto
 */
bool IsValidURLScheme(const char *scheme);

/**
 * Returns whether the given string has a valid url prefixes.
 *
 * Valid url prefixes are:
 * http://
 * https://
 * feed://
 * file://
 * mailto:
 */
bool HasValidURLPrefix(const char *url);

/**
 * Returns whether the given string is a valid url component,
 * or in another word, if it only contains valid url chars.
 */
bool IsValidURLComponent(const char *url);

/**
 * Returns whether the given string only contains valid url chars.
 */
bool IsValidURLString(const char *url);

/**
 * Returns whether the given string is a valid URL.
 *
 * Equals to HasValidURLPrefix(url) && IsValidURLString(url)
 */
bool IsValidURL(const char *url);

/** Returns whether the given string is a valid URL for a RSS feed. */
bool IsValidRSSURL(const char *url);

/**
 * Returns whether the given string is a valid URL.
 * Only http:// and https:// prefix are allowed.
 * Not a very complete check at the moment.
 */
bool IsValidWebURL(const char *url);

/**
 * Returns whether the given string is a valid file URL,
 * which has file:// prefix.
 */
bool IsValidFileURL(const char *url);

/**
 * Returns the host part of a URL in common Internet scheme syntax:
 * <scheme>://[<user>:<password>@]<host>[:<port>][/<url_path>].
 * Returns blank string if the URL is invalid.
 */
std::string GetHostFromURL(const char *url);

/**
 * Returns the filename part of a file URL, or blank string if the url is not a
 * valid file url.
 */
std::string GetPathFromFileURL(const char *url);

/**
 * Returns the username:password part of a URL, or blank string if the url has
 * no username:password part.
 */
std::string GetUsernamePasswordFromURL(const char *url);

/**
 * @param base_url the base URL (must be absolute).
 * @param url an relative or absolute URL.
 * @return the absolute URL computed from @a base_url and @a url.
 */
std::string GetAbsoluteURL(const char *base_url, const char *url);

/**
 * Splits a string into two parts. For convenience, the impl allows
 * @a result_left or @a result_right is the same object as @a source.
 *
 * @param source the source string to split.
 * @param separator the source string will be split at the first occurrence
 *     of the separator.
 * @param[out] result_left the part before the separator. If separator is not
 *     found, result_left will be set to source. Can be @c NULL if the caller
 *     doesn't need it.
 * @param[out] result_right the part after the separator. If separator is not
 *     found, result_right will be cleared. Can be @c NULL if the caller doesn't
 *     need it.
 * @return @c true if separator found.
 */
bool SplitString(const std::string &source, const char *separator,
                 std::string *result_left, std::string *result_right);

/**
 * Splits a string into a list with specified separator.
 * @param source the source string to split.
 * @param separator the separator string to be used to split the source string.
 * @param[out] result store the result string list.
 * @return @c true if separator found.
 */
bool SplitStringList(const std::string &source, const char *separator,
                     StringVector *result);

/**
 * Compresses white spaces in a string using the rule like HTML formatting:
 *   - Removing leading and trailing white spaces;
 *   - Converting all consecutive white spaces into single spaces;
 * Only ASCII spaces (isspace(ch) == true) are handled.
 */
std::string CompressWhiteSpaces(const char *source);

/**
 * Removes tags and converts entities to their utf8 representation.
 * If everything is removed, this will return an empty string.
 * Whitespaces are compressed as in @c CompressWhiteSpaces().
 */
std::string ExtractTextFromHTML(const char *source);

/**
 * Guess if a string contains HTML. We basically check for common constructs
 * in html such as </, />, <br>, <hr>, <p>, etc.
 * This function only scans the 50k characters as an optimization.
 */
bool ContainsHTML(const char *s);

/**
 * Converts all '\r's, '\n's and '\r\n's into spaces. Useful to display
 * multi-line text in a single-line container.
 */
std::string CleanupLineBreaks(const char *source);

/**
 * Matches an XPath string against an XPath pattern, and returns whether
 * matches. This function only supports simple xpath grammar, containing only
 * element tag name, element index (not allowed in pattern) and attribute
 * names, no wildcard or other xpath expressions.
 *
 * @param xpath an xpath string returned as one of the keys in the result of
 *     XMLParserInterface::ParseXMLIntoXPathMap().
 * @param pattern an xpath pattern with only element tag names and (optional)
 *     attribute names.
 * @return true if the xpath matches the pattern. The matching rule is: first
 *     remove all [...]s in the xpath, and test if the result equals to the
 *     pattern.
 */
bool SimpleMatchXPath(const char *xpath, const char *pattern);

/**
 * Compares two versions.
 * @param version1 version string in "x", "x.x", "x.x.x" or "x.x.x.x" format
 *     where 'x' is an integer.
 * @param version2
 * @param[out] result on success: -1 if version1 < version2, 0 if
 *     version1 == version2, or 1 if version1 > version2.
 * @return @c false if @a version1 or @a version2 is invalid version string,
 *     or @c true on success.
 */
bool CompareVersion(const char *version1, const char *version2, int *result);

/** Checks if a string has a specified prefix. */
bool StartWith(const char *string, const char *prefix);

/** Checks if a string has a specified prefix, ignoring the case. */
bool StartWithNoCase(const char *string, const char *prefix);

/** Checks if a string has a specified suffix. */
bool EndWith(const char *string, const char *suffix);

/** Checks if a string has a specified suffix, ignoring the case. */
bool EndWithNoCase(const char *string, const char *suffix);

#endif
