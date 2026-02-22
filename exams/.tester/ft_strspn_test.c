#include <stdio.h>
#include <stddef.h>
#include <string.h>

size_t	ft_strspn(const char *s, const char *accept);

static int	failed = 0;

static void	check(size_t got, size_t expected, const char *name)
{
	if (got != expected)
	{
		printf("FAIL [%s]: got %zu, expected %zu\n", name, got, expected);
		failed++;
	}
}

int	main(void)
{
	check(ft_strspn("hello", "helo"), 5, "all match");
	check(ft_strspn("hello", "h"), 1, "only first");
	check(ft_strspn("hello", ""), 0, "empty accept");
	check(ft_strspn("", "abc"), 0, "empty s");
	check(ft_strspn("hello", "jfkhpell"), 4, "subject example");
	check(ft_strspn("abc", "xyz"), 0, "no match");
	check(ft_strspn("aaaaab", "a"), 5, "repeated char");
	check(ft_strspn("hello world", "helo"), 5, "stops at space");
	check(ft_strspn("12345", "1234567890"), 5, "digits all match");
	check(ft_strspn("abcdef", "abc"), 3, "partial match");
	check(ft_strspn("zyxwv", "abcdefghijklmnopqrstuvwxyz"), 5, "all alpha");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
