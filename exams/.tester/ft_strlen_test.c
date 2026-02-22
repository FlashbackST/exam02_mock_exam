#include <stdio.h>
#include <string.h>

int	ft_strlen(char *str);

static int	failed = 0;

static void	check(int got, int expected, const char *name)
{
	if (got != expected)
	{
		printf("FAIL [%s]: got %d, expected %d\n", name, got, expected);
		failed++;
	}
}

int	main(void)
{
	check(ft_strlen("hello"), 5, "hello");
	check(ft_strlen(""), 0, "empty string");
	check(ft_strlen("a"), 1, "single char");
	check(ft_strlen("Hello World"), 11, "with space");
	check(ft_strlen("42"), 2, "number string");
	check(ft_strlen("abcdefghij"), 10, "10 chars");
	check(ft_strlen("\t\n"), 2, "escape chars");
	check(ft_strlen("!@#$%"), 5, "special chars");
	check(ft_strlen("   "), 3, "spaces only");
	check(ft_strlen("0"), 1, "zero char");
	check(ft_strlen("longstringwithmanycharstotest"), 29, "long string");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
