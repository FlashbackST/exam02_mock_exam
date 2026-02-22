#include <stdio.h>
#include <stdlib.h>

int	*ft_rrange(int start, int end);

static int	failed = 0;

/*
** ft_rrange returns values starting from end going towards start.
** ft_rrange(1, 3) = {3, 2, 1}
** ft_rrange(0, -3) = {-3, -2, -1, 0}
*/
static void	check(int start, int end, const char *name)
{
	int	*r;
	int	len;
	int	step;
	int	i;
	int	expected;

	r = ft_rrange(start, end);
	len = (start <= end) ? (end - start + 1) : (start - end + 1);
	/* When start<=end, values go end, end-1, ..., start → step = -1
	** When start>end, values go end, end+1, ..., start → step = +1 */
	step = (start <= end) ? -1 : 1;

	if (r == NULL)
	{
		printf("FAIL [%s]: returned NULL\n", name);
		failed++;
		return;
	}
	i = 0;
	while (i < len)
	{
		expected = end + i * step;
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
	check(0, -3, "0 to -3");
	check(0, 5, "0 to 5");
	check(-3, 3, "-3 to 3");
	check(10, 5, "10 to 5");
	check(-5, 0, "-5 to 0");
	check(100, 105, "100 to 105");
	check(-10, -5, "-10 to -5");

	/* Single element */
	r = ft_rrange(7, 7);
	if (r == NULL || r[0] != 7)
	{
		printf("FAIL [single 7]: r[0]=%d\n", r ? r[0] : -1);
		failed++;
	}
	if (r) free(r);

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
