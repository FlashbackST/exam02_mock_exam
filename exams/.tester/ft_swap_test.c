#include <stdio.h>

void	ft_swap(int *a, int *b);

static int	failed = 0;

static void	check(int a, int b, int ea, int eb, const char *name)
{
	if (a != ea || b != eb)
	{
		printf("FAIL [%s]: got a=%d b=%d, expected a=%d b=%d\n", name, a, b, ea, eb);
		failed++;
	}
}

int	main(void)
{
	int	a;
	int	b;

	a = 1; b = 2; ft_swap(&a, &b);
	check(a, b, 2, 1, "1,2");

	a = 0; b = 0; ft_swap(&a, &b);
	check(a, b, 0, 0, "0,0");

	a = -1; b = 1; ft_swap(&a, &b);
	check(a, b, 1, -1, "-1,1");

	a = 42; b = 21; ft_swap(&a, &b);
	check(a, b, 21, 42, "42,21");

	a = 100; b = -100; ft_swap(&a, &b);
	check(a, b, -100, 100, "100,-100");

	a = 0; b = 5; ft_swap(&a, &b);
	check(a, b, 5, 0, "0,5");

	a = -5; b = -10; ft_swap(&a, &b);
	check(a, b, -10, -5, "-5,-10");

	a = 2147483647; b = -2147483648; ft_swap(&a, &b);
	check(a, b, -2147483648, 2147483647, "INT_MAX,INT_MIN");

	a = 7; b = 7; ft_swap(&a, &b);
	check(a, b, 7, 7, "same values");

	a = 1000; b = 2000; ft_swap(&a, &b);
	check(a, b, 2000, 1000, "1000,2000");

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
