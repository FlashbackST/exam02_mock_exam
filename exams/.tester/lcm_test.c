#include <stdio.h>

unsigned int	lcm(unsigned int a, unsigned int b);

static int	failed = 0;

static void	check(unsigned int got, unsigned int expected, const char *name)
{
	if (got != expected)
	{
		printf("FAIL [%s]: got %u, expected %u\n", name, got, expected);
		failed++;
	}
}

int	main(void)
{
	check(lcm(4, 6), 12, "lcm(4,6)=12");
	check(lcm(3, 5), 15, "lcm(3,5)=15");
	check(lcm(1, 1), 1, "lcm(1,1)=1");
	check(lcm(6, 4), 12, "lcm(6,4)=12 commutative");
	check(lcm(0, 5), 0, "lcm(0,5)=0");
	check(lcm(5, 0), 0, "lcm(5,0)=0");
	check(lcm(12, 18), 36, "lcm(12,18)=36");
	check(lcm(7, 7), 7, "lcm(7,7)=7");
	check(lcm(2, 3), 6, "lcm(2,3)=6");
	check(lcm(100, 75), 300, "lcm(100,75)=300");
	check(lcm(5, 15), 15, "lcm(5,15)=15 divisible");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
