#include <stdio.h>

unsigned char	reverse_bits(unsigned char octet);

static int	failed = 0;

static void	check(unsigned char got, unsigned char expected, const char *name)
{
	if (got != expected)
	{
		printf("FAIL [%s]: got %d, expected %d\n", name, got, expected);
		failed++;
	}
}

int	main(void)
{
	check(reverse_bits(0), 0, "0");
	check(reverse_bits(255), 255, "255");
	check(reverse_bits(1), 128, "1->128");
	check(reverse_bits(128), 1, "128->1");
	check(reverse_bits(2), 64, "2->64");
	check(reverse_bits(64), 2, "64->2");
	check(reverse_bits(42), 84, "42->84");
	check(reverse_bits(85), 170, "85->170");
	check(reverse_bits(170), 85, "170->85");
	check(reverse_bits(16), 8, "16->8");
	check(reverse_bits(3), 192, "3->192");
	check(reverse_bits(127), 254, "127->254");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
