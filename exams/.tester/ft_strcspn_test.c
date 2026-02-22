#include <stdio.h>
#include <stddef.h>

size_t	ft_strcspn(const char *s, const char *reject);

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
	check(ft_strcspn("hello", "l"), 2, "first l");
	check(ft_strcspn("hello", "xyz"), 5, "no match");
	check(ft_strcspn("hello", ""), 5, "empty reject");
	check(ft_strcspn("", "abc"), 0, "empty s");
	check(ft_strcspn("abcdef", "c"), 2, "middle char");
	check(ft_strcspn("hello world", " "), 5, "space separator");
	check(ft_strcspn("12345", "3"), 2, "digit");
	check(ft_strcspn("aabbcc", "b"), 2, "repeated");
	check(ft_strcspn("hello", "h"), 0, "first char");
	check(ft_strcspn("hello", "o"), 4, "last char");
	check(ft_strcspn("abcdef", "fg"), 5, "two in reject");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
