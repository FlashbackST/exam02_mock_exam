#include <stdio.h>
#include <stdlib.h>

int	*ft_range(int start, int end);

static int	failed = 0;

/* Both start and end are inclusive. If start > end, values decrease. */
static void	check(int start, int end, const char *name)
{
	int	*r;
	int	len;
	int	step;
	int	i;
	int	expected;

	r = ft_range(start, end);
	len = (start <= end) ? (end - start + 1) : (start - end + 1);
	step = (start <= end) ? 1 : -1;

	if (r == NULL)
	{
		printf("FAIL [%s]: returned NULL\n", name);
		failed++;
		return;
	}
	i = 0;
	while (i < len)
	{
		expected = start + i * step;
		if (r[i] != expected)
		{
			printf("FAIL [%s]: r[%d]=%d, expected %d\n", name, i, r[i], expected);
			failed++;
			free(r);
			return;
		}
		i++;
	}
	free(r);
}

int	main(void)
{
	int	*r;

	check(1, 3, "1 to 3");
	check(-1, 2, "-1 to 2");
	check(0, 0, "start==end");
	check(0, -3, "0 to -3 (decreasing)");
	check(0, 5, "0 to 5");
	check(-3, 3, "-3 to 3");
	check(10, 5, "10 to 5 (decreasing)");
	check(-5, 0, "-5 to 0");
	check(100, 105, "100 to 105");
	check(-10, -5, "-10 to -5");

	/* Single element: start==end */
	r = ft_range(42, 42);
	if (r == NULL || r[0] != 42)
	{
		printf("FAIL [single 42]: r[0]=%d\n", r ? r[0] : -1);
		failed++;
	}
	if (r) free(r);

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
