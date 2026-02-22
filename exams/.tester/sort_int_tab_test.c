#include <stdio.h>
#include <string.h>

void	sort_int_tab(int *tab, unsigned int size);

static int	failed = 0;

static void	check_sorted(int *tab, unsigned int size, const char *name)
{
	unsigned int	i;

	i = 0;
	while (i + 1 < size)
	{
		if (tab[i] > tab[i + 1])
		{
			printf("FAIL [%s]: not sorted at index %u (%d > %d)\n",
				name, i, tab[i], tab[i + 1]);
			failed++;
			return;
		}
		i++;
	}
}

int	main(void)
{
	int	t1[] = {5, 3, 1, 4, 2};
	int	t2[] = {1, 2, 3, 4, 5};
	int	t3[] = {5, 4, 3, 2, 1};
	int	t4[] = {42};
	int	t5[] = {2, 1};
	int	t6[] = {1, 21, 9, 4, 30, 8, 4, 7, 42, 11};
	int	t7[] = {-5, -1, -3, -2, -4};
	int	t8[] = {0, 0, 0, 0};
	int	t9[] = {-3, 5, -1, 4, 0};
	int	t10[] = {100, -100, 0, 50, -50};

	sort_int_tab(t1, 5); check_sorted(t1, 5, "random 5");
	sort_int_tab(t2, 5); check_sorted(t2, 5, "already sorted");
	sort_int_tab(t3, 5); check_sorted(t3, 5, "reverse sorted");
	sort_int_tab(t4, 1); check_sorted(t4, 1, "single element");
	sort_int_tab(t5, 2); check_sorted(t5, 2, "two elements");
	sort_int_tab(t6, 10); check_sorted(t6, 10, "10 elements");
	sort_int_tab(t7, 5); check_sorted(t7, 5, "all negative");
	sort_int_tab(t8, 4); check_sorted(t8, 4, "all zeros");
	sort_int_tab(t9, 5); check_sorted(t9, 5, "mixed neg/pos");
	sort_int_tab(t10, 5); check_sorted(t10, 5, "100,-100,0,50,-50");
	sort_int_tab(NULL, 0);  /* should not crash */
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
