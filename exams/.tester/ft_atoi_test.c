#include <stdio.h>

int	ft_atoi(const char *str);

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
	check(ft_atoi("0"), 0, "zero");
	check(ft_atoi("42"), 42, "42");
	check(ft_atoi("-42"), -42, "-42");
	check(ft_atoi("+42"), 42, "+42");
	check(ft_atoi("   42"), 42, "leading spaces");
	check(ft_atoi("  -42"), -42, "leading spaces neg");
	check(ft_atoi("2147483647"), 2147483647, "INT_MAX");
	check(ft_atoi("-2147483648"), -2147483648, "INT_MIN");
	check(ft_atoi("42abc"), 42, "trailing chars");
	check(ft_atoi(""), 0, "empty");
	check(ft_atoi("   "), 0, "spaces only");
	check(ft_atoi("1"), 1, "one");
	check(ft_atoi("-1"), -1, "minus one");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
