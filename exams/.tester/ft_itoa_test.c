#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	*ft_itoa(int nbr);

static int	failed = 0;

static void	check(int n, const char *expected, const char *name)
{
	char	*got = ft_itoa(n);

	if (got == NULL)
	{
		printf("FAIL [%s]: returned NULL\n", name);
		failed++;
		return;
	}
	if (strcmp(got, expected) != 0)
	{
		printf("FAIL [%s]: got \"%s\", expected \"%s\"\n", name, got, expected);
		failed++;
	}
	free(got);
}

int	main(void)
{
	check(0, "0", "zero");
	check(42, "42", "42");
	check(-42, "-42", "-42");
	check(1, "1", "one");
	check(-1, "-1", "minus one");
	check(2147483647, "2147483647", "INT_MAX");
	check(-2147483648, "-2147483648", "INT_MIN");
	check(100, "100", "100");
	check(-100, "-100", "-100");
	check(1000000, "1000000", "one million");
	check(123456789, "123456789", "large");
	check(-987654321, "-987654321", "large negative");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
