#include <stdio.h>

int	is_power_of_2(unsigned int n);

static int	failed = 0;

static void	check(int got, int expected, const char *name)
{
	if (!got != !expected)
	{
		printf("FAIL [%s]: got %d, expected %d\n", name, got, expected);
		failed++;
	}
}

int	main(void)
{
	check(is_power_of_2(0), 0, "0 is not power of 2");
	check(is_power_of_2(1), 1, "1 is power of 2");
	check(is_power_of_2(2), 1, "2");
	check(is_power_of_2(3), 0, "3");
	check(is_power_of_2(4), 1, "4");
	check(is_power_of_2(5), 0, "5");
	check(is_power_of_2(8), 1, "8");
	check(is_power_of_2(16), 1, "16");
	check(is_power_of_2(32), 1, "32");
	check(is_power_of_2(64), 1, "64");
	check(is_power_of_2(128), 1, "128");
	check(is_power_of_2(256), 1, "256");
	check(is_power_of_2(1024), 1, "1024");
	check(is_power_of_2(1023), 0, "1023");
	check(is_power_of_2(2147483648u), 1, "2^31");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
