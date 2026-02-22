#include <stdio.h>

int	ft_atoi_base(const char *str, int str_base);

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
	check(ft_atoi_base("42", 10), 42, "base10 42");
	check(ft_atoi_base("101010", 2), 42, "base2 101010=42");
	check(ft_atoi_base("2a", 16), 42, "base16 2a=42");
	check(ft_atoi_base("52", 8), 42, "base8 52=42");
	check(ft_atoi_base("0", 10), 0, "zero base10");
	check(ft_atoi_base("0", 2), 0, "zero base2");
	check(ft_atoi_base("-42", 10), -42, "negative base10");
	check(ft_atoi_base("-2a", 16), -42, "negative base16");
	check(ft_atoi_base("ff", 16), 255, "ff=255");
	check(ft_atoi_base("FF", 16), 255, "FF=255");
	check(ft_atoi_base("1", 10), 1, "one");
	check(ft_atoi_base("   42", 10), 42, "leading spaces");
	check(ft_atoi_base("+10", 10), 10, "plus sign");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
