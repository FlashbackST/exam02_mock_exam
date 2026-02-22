#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifndef T_POINT_H
# define T_POINT_H
typedef struct s_point
{
	int	x;
	int	y;
}	t_point;
#endif

void	flood_fill(char **tab, t_point size, t_point begin);

static int	failed = 0;

static char	**make_grid(const char *rows[], int height)
{
	char	**grid = malloc(sizeof(char *) * (height + 1));
	int		i;

	i = 0;
	while (i < height)
	{
		grid[i] = strdup(rows[i]);
		i++;
	}
	grid[height] = NULL;
	return (grid);
}

static void	free_grid(char **grid, int height)
{
	int	i;

	i = 0;
	while (i < height)
		free(grid[i++]);
	free(grid);
}

static void	check_grid(char **grid, const char *expected[], int height, const char *name)
{
	int	i;

	i = 0;
	while (i < height)
	{
		if (strcmp(grid[i], expected[i]) != 0)
		{
			printf("FAIL [%s] row %d: got \"%s\", expected \"%s\"\n",
				name, i, grid[i], expected[i]);
			failed++;
			return;
		}
		i++;
	}
}

int	main(void)
{
	/* Test 1: basic flood fill - subject example */
	const char	*in1[] = {
		"11111111",
		"10001001",
		"10010001",
		"10110001",
		"11100001",
	};
	const char	*ex1[] = {
		"11111111",
		"1FFF1001",
		"1FF10001",
		"1F110001",
		"11100001",
	};
	char	**g1 = make_grid(in1, 5);
	t_point	size1 = {8, 5};
	t_point	begin1 = {2, 2};
	flood_fill(g1, size1, begin1);
	check_grid(g1, ex1, 5, "subject example");
	free_grid(g1, 5);

	/* Test 2: fill entire grid */
	const char	*in2[] = {
		"0000",
		"0000",
		"0000",
	};
	const char	*ex2[] = {
		"FFFF",
		"FFFF",
		"FFFF",
	};
	char	**g2 = make_grid(in2, 3);
	t_point	size2 = {4, 3};
	t_point	begin2 = {0, 0};
	flood_fill(g2, size2, begin2);
	check_grid(g2, ex2, 3, "fill all");
	free_grid(g2, 3);

	/* Test 3: isolated cell - '0' in center, '0' also in corners (connected via edges) */
	/* 010   begin (1,1)='0' connects to (0,1),(2,1),(1,0)='1' stop,(1,2)='1' stop  */
	/* 000   (0,1) connects to (0,0),(0,2); (2,1) connects to (2,0),(2,2)           */
	/* 010   Result: all '0's fill since they are all connected through middle row   */
	const char	*in3[] = {
		"010",
		"000",
		"010",
	};
	const char	*ex3[] = {
		"F1F",
		"FFF",
		"F1F",
	};
	char	**g3 = make_grid(in3, 3);
	t_point	size3 = {3, 3};
	t_point	begin3 = {1, 1};
	flood_fill(g3, size3, begin3);
	check_grid(g3, ex3, 3, "connected zeros");
	free_grid(g3, 3);

	/* Test 4: fill from corner - (3,1) connects through (3,0) */
	const char	*in4[] = {
		"00001",
		"00101",
		"01111",
	};
	const char	*ex4[] = {
		"FFFF1",
		"FF1F1",
		"F1111",
	};
	char	**g4 = make_grid(in4, 3);
	t_point	size4 = {5, 3};
	t_point	begin4 = {0, 0};
	flood_fill(g4, size4, begin4);
	check_grid(g4, ex4, 3, "corner fill");
	free_grid(g4, 3);

	/* Test 5: single cell - only one cell with that char */
	const char	*in5[] = {
		"111",
		"1F1",
		"111",
	};
	const char	*ex5[] = {
		"111",
		"1F1",
		"111",
	};
	char	**g5 = make_grid(in5, 3);
	t_point	size5 = {3, 3};
	t_point	begin5 = {1, 1};
	flood_fill(g5, size5, begin5);
	check_grid(g5, ex5, 3, "single cell F");
	free_grid(g5, 3);

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
