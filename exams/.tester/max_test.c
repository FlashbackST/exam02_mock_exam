#include <stdio.h>

int	max(int *tab, unsigned int len);

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
	int	t1[] = {1, 2, 3, 4, 5};
	int	t2[] = {5, 4, 3, 2, 1};
	int	t3[] = {42};
	int	t4[] = {-1, -2, -3};
	int	t5[] = {0, 0, 0};
	int	t6[] = {-5, 10, -3, 7};
	int	t7[] = {2147483647, 0, -1};
	int	t8[] = {-2147483648, 0};
	int	t9[] = {1, 1, 1, 2};
	int	t10[] = {100, 50, 75, 25};

	check(max(t1, 5), 5, "ascending");
	check(max(t2, 5), 5, "descending");
	check(max(t3, 1), 42, "single element");
	check(max(t4, 3), -1, "all negative");
	check(max(t5, 3), 0, "all zeros");
	check(max(t6, 4), 10, "mixed");
	check(max(t7, 3), 2147483647, "INT_MAX");
	check(max(t8, 2), 0, "INT_MIN and 0");
	check(max(t9, 4), 2, "almost all same");
	check(max(t10, 4), 100, "100 first");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
