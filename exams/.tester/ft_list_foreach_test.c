#include <stdio.h>
#include <stdlib.h>

#ifndef FT_LIST_H
# define FT_LIST_H
typedef struct s_list
{
	struct s_list	*next;
	void			*data;
}	t_list;
#endif

void	ft_list_foreach(t_list *begin_list, void (*f)(void *));

static int	failed = 0;
static int	counter = 0;
static int	sum = 0;

static void	count_node(void *data)
{
	(void)data;
	counter++;
}

static void	add_to_sum(void *data)
{
	sum += (int)(long)data;
}

static t_list	*make_node(void *data, t_list *next)
{
	t_list	*node = malloc(sizeof(t_list));

	node->data = data;
	node->next = next;
	return (node);
}

static void	free_list(t_list *lst)
{
	t_list	*tmp;

	while (lst)
	{
		tmp = lst->next;
		free(lst);
		lst = tmp;
	}
}

int	main(void)
{
	t_list	*lst;

	/* Test 1: count elements */
	counter = 0;
	lst = make_node(NULL, make_node(NULL, make_node(NULL, NULL)));
	ft_list_foreach(lst, count_node);
	if (counter != 3)
	{
		printf("FAIL [count 3 nodes]: got %d, expected 3\n", counter);
		failed++;
	}
	free_list(lst);

	/* Test 2: NULL list should not crash */
	counter = 0;
	ft_list_foreach(NULL, count_node);
	if (counter != 0)
	{
		printf("FAIL [NULL list]: function was called\n");
		failed++;
	}

	/* Test 3: single element */
	counter = 0;
	lst = make_node(NULL, NULL);
	ft_list_foreach(lst, count_node);
	if (counter != 1)
	{
		printf("FAIL [single node]: got %d, expected 1\n", counter);
		failed++;
	}
	free_list(lst);

	/* Test 4: sum of values */
	sum = 0;
	lst = make_node((void*)1L, make_node((void*)2L, make_node((void*)3L, NULL)));
	ft_list_foreach(lst, add_to_sum);
	if (sum != 6)
	{
		printf("FAIL [sum 1+2+3]: got %d, expected 6\n", sum);
		failed++;
	}
	free_list(lst);

	/* Test 5: 5 elements count */
	counter = 0;
	lst = make_node(NULL, make_node(NULL,
		make_node(NULL, make_node(NULL, make_node(NULL, NULL)))));
	ft_list_foreach(lst, count_node);
	if (counter != 5)
	{
		printf("FAIL [count 5 nodes]: got %d, expected 5\n", counter);
		failed++;
	}
	free_list(lst);

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
